import { Fragment, useEffect, useRef } from "react";
import PulseLoader from "react-spinners/PulseLoader";
import Message from "./message";
import { Item } from "~/types";

export default function Messages(
    { 
        items, 
        isProcessing 
    } : 
    { 
        items: Item[], 
        isProcessing: boolean 
    }
) {
  const messagesEndRef = useRef(null); // just used to scroll to the bottom of the messages

  useEffect(() => {
    if (items.length > 2) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [items.length]);

  return (
    <section className="w-full">
      {items.map((ev, index) => {
        if (ev.video_carousel) {
          return (
            // video carousel
            <div>Empty for now</div>
          );
        }

        if (ev.prompt) {
          return (
            <Message key={"prompt-" + index} sender={ev.sender}>
              {ev.prompt}
            </Message>
          );
        }
      })}

      {isProcessing && (
        <Message sender="system">
          <PulseLoader color="#999" size={7} />
        </Message>
      )}

      <div ref={messagesEndRef} />
    </section>
  );
}
