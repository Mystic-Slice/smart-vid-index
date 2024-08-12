import { SquareArrowOutUpRight, Trash2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Id, toast } from "react-toastify";
import Messages from "~/components/messages";
import PromptForm from "~/components/promptform";
import Sidebar from "~/components/sidebar";
import { ScrollArea } from "~/components/ui/scroll-area";
import { Item } from "~/types";
import { apiReq } from "~/utils";

export default function Chat() {
    const [messageItems, setMessageItems] = useState<Item[]>([]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState(null);
    const [initialPrompt, setInitialPrompt] = useState("");

    const [sidebarItems, setSidebarItems] = useState([]);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isSidebarProcessing, setIsSidebarProcessing] = useState(false);
    const [isAdding, setIsAdding] = useState(false);

    const toastId = useRef<Id | null>(null);

    const toggleSidebar = () => {
      setIsSidebarOpen(!isSidebarOpen);
    };

    const deleteItem = async (item: any) => {
        toastId.current = toast("Deleting video...", {autoClose: false});
        console.log("Deleting item:", item.video_id);
        const result = await apiReq("sidebar", { "query": "deleteItem", "video_id": item.video_id });
        if (result.error) {
            setError(result.error);
            toast.update(
                toastId.current,
                {
                    render: result.error,
                    type: 'error',
                    autoClose: 5000
                }
            )
            toastId.current = null;
            return;
        }
        console.log(result);

        toast.update(
            toastId.current,
            {
                render: "Video deleted successfully",
                type: 'success',
                autoClose: 5000
            }
        )

        toastId.current = null;
        refreshSidebar();
    }
    const linkToItem = async (item: any) => {
        const url = item.video_url ? item.video_url : `https://youtube.com/watch?v=${item.video_id}`;
        window.open(url, "_blank");
    }
    const addItem  = async (url: string) => {
        toastId.current = toast("Adding video...", {autoClose: false});

        setIsAdding(true);
        console.log("Adding item:", url);
        const result = await apiReq("sidebar", { "query": "addItem", "url": url });
        if (result.error) {
            setError(result.error);
            toast.update(
                toastId.current,
                {
                    render: result.error,
                    type: 'error',
                    autoClose: 5000
                }
            )
            toastId.current = null;
            return;
        }
        console.log(result);
        setIsAdding(false);

        toast.update(
            toastId.current,
            {
                render: "Video added successfully",
                type: 'success',
                autoClose: 5000
            }
        )
        refreshSidebar();
    }
    const itemActions = [
        {
            handler: deleteItem,
            label: "Delete",
            icon: <Trash2/>,
        },
        {
            handler: linkToItem,
            label: "Link",
            icon: <SquareArrowOutUpRight/>,
        }        
    ]

    const refreshSidebar = async () => {
        setIsSidebarProcessing(true);
        const result = await apiReq("sidebar", { "query": "getItems" });
        if (result.error) {
            setError(result.error);
            setIsProcessing(false);
            return;
        }

        const newSidebarItems = result.videos;
        setSidebarItems(newSidebarItems);
        setIsSidebarProcessing(false);
    }

    useEffect(() => {
        setMessageItems([
            {
                prompt: "How can I help you?",
                sender: "system",
            },
        ]);
        refreshSidebar();
    }, []);

    const handleSubmit = async (e: any) => {
        const prompt = e.target.prompt.value as string;

        setError(null);
        setIsProcessing(true);
        setInitialPrompt("");

        const currMessageItems = [...messageItems, { prompt, sender: "user" } as Item];
        setMessageItems(currMessageItems);

        const body = { query: prompt };

        const result = await apiReq("search", body);
        console.log(result)

        if (result.error) {
            setError(result.error);
            setIsProcessing(false);
            return;
        }
        
        const response = result.response;

        const answer = response.answer;
        const links = response.links;

        currMessageItems.push({ prompt: answer, sender: "system" } as Item);
        currMessageItems.push({ video_carousel_links: links, sender: "system" } as Item);

        setMessageItems(currMessageItems);
        setIsProcessing(false);
    }

    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar 
                isOpen={isSidebarOpen} 
                items={sidebarItems} 
                isProcessing={isSidebarProcessing}
                title="Your Video Collection"
                itemActions={itemActions}
                addItem={addItem}
                isAdding={isAdding}
            />
            <div className={`h-full flex-grow transition-all duration-300 ${isSidebarOpen ? 'ml-[30%]' : 'ml-32'} p-6 flex flex-col`}>
                <ScrollArea className="flex-grow bg-slate-400" invisibleScrollbar={true}>
                    <Messages
                        items={messageItems}
                        isProcessing={isProcessing}
                    />
                </ScrollArea>
                <PromptForm
                    initialPrompt={initialPrompt}
                    isFirstPrompt={messageItems.length === 1}
                    onSubmit={(e: any) => {
                        console.log("Prompt submitted:", e.target.prompt.value);
                        handleSubmit(e);
                    }}
                />
                {/* <div className="mx-auto w-full">
                    {error && <p className="bold text-red-500 pb-5">{error}</p>}
                </div> */}
            </div>
            <button 
                onClick={toggleSidebar}
                className={`absolute top-4 transition-all duration-300
                    ${isSidebarOpen ? 'left-[calc(30%-1.25rem)]' : 'left-[calc(8rem-1.25rem)]'}
                    z-50 bg-gray-800 text-white rounded-full w-10 h-10 flex items-center justify-center
                    focus:outline-none hover:bg-gray-700`}>
                {isSidebarOpen ? '◀' : '▶'}
            </button>
        </div>
    )
}