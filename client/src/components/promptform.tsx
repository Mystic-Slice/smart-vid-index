import { ArrowUp } from "lucide-react";
import { useEffect, useState } from "react";
import Message from "./message";

export default function PromptForm({
    initialPrompt = "default prompt",
    isFirstPrompt,
    onSubmit,
    disabled,
  } :
  {
    initialPrompt: string,
    isFirstPrompt?: boolean,
    onSubmit: (e: any) => void,
    disabled?: boolean
  }
) {
    const [prompt, setPrompt] = useState(initialPrompt);
  
    useEffect(() => {
      setPrompt(initialPrompt);
    }, [initialPrompt]);
  
    const handleSubmit = (e: any) => {
      e.preventDefault();
      setPrompt("");
      onSubmit(e);
    };
  
    if (disabled) {
      return;
    }
  
    return (
      <form onSubmit={handleSubmit} className="animate-in fade-in duration-700">
        <div className="flex mt-2">
          <input
            id="prompt-input"
            type="text"
            name="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Your message..."
            className={`block w-full flex-grow p-4${
              disabled ? " rounded-md" : " rounded-l-md"
            }`}
            disabled={disabled}
          />
  
          {disabled || (
            <button
              className="bg-black text-white rounded-r-md text-small inline-block p-3 flex-none"
              type="submit"
            >
              <ArrowUp />
            </button>
          )}
        </div>
      </form>
    );
  }