import { useEffect, useState } from "react";
import Messages from "~/components/messages";
import PromptForm from "~/components/promptform";
import { Item } from "~/types";
import { apiReq } from "~/utils";

export default function Chat() {
    const [items, setItems] = useState<Item[]>([]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState(null);
    const [initialPrompt, setInitialPrompt] = useState("");

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

        setItems([...myItems, { prompt: answer, sender: "system" } as Item]);
        setIsProcessing(false);
    }

    return (
        <div>
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
    )
}