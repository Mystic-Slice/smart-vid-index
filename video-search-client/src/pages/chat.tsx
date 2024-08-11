import { useEffect, useState } from "react";
import Messages from "~/components/messages";
import PromptForm from "~/components/promptform";
import Sidebar from "~/components/sidebar";
import { Item } from "~/types";
import { apiReq } from "~/utils";

const menuItems = [
    "Home",
    "Profile",
    "Settings",
    "Messages"
];

export default function Chat() {
    const [items, setItems] = useState<Item[]>([]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState(null);
    const [initialPrompt, setInitialPrompt] = useState("");

    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    const toggleSidebar = () => {
      setIsSidebarOpen(!isSidebarOpen);
    };

    useEffect(() => {
        setItems([
            {
                prompt: "How can I help you?",
                sender: "system",
            },
        ]);
    }, []);

    const handleSubmit = async (e: any) => {
        const prompt = e.target.prompt.value as string;

        setError(null);
        setIsProcessing(true);
        setInitialPrompt("");

        const myItems = [...items, { prompt, sender: "user" } as Item];
        setItems(myItems);

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

        myItems.push({ prompt: answer, sender: "system" } as Item);
        myItems.push({ video_carousel_links: links, sender: "system" } as Item);

        setItems(myItems);
        setIsProcessing(false);
    }

    // divide page into two columns


    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar isOpen={isSidebarOpen} menuItems={menuItems}/>
            <div className={`flex-grow transition-all duration-300 ${isSidebarOpen ? 'ml-[30%]' : 'ml-16'}`}>
                <Messages
                    items={items}
                    isProcessing={isProcessing}
                />
                <PromptForm
                    initialPrompt={initialPrompt}
                    isFirstPrompt={items.length === 1}
                    onSubmit={(e: any) => {
                        console.log("Prompt submitted:", e.target.prompt.value);
                        handleSubmit(e);
                    }}
                />
                <div className="mx-auto w-full">
                    {error && <p className="bold text-red-500 pb-5">{error}</p>}
                </div>
            </div>
            <button 
                onClick={toggleSidebar}
                className={`absolute top-4 transition-all duration-300
                    ${isSidebarOpen ? 'left-[calc(20%-1.25rem)]' : 'left-[calc(4rem-1.25rem)]'}
                    z-50 bg-gray-800 text-white rounded-full w-10 h-10 flex items-center justify-center
                    focus:outline-none hover:bg-gray-700`}>
                {isSidebarOpen ? '◀' : '▶'}
            </button>
        </div>
    )
}