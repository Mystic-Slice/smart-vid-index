import { Item } from "~/types";

export default function Message({
    sender,
    shouldFillWidth,
    isSameSender,
    children,
  }: {
    sender: Item["sender"],
    shouldFillWidth?: boolean,
    isSameSender?: boolean,
    children: React.ReactNode,
  }) {
    return (
      <div className={`w-full ${sender === "user" ? "text-right" : ""}`}>
        <div
          className={`p-3 rounded-lg ${shouldFillWidth ? "" : "inline-block"} ${
            sender === "user"
              ? "ml-16 bg-blue-600 text-white"
              : "bg-gray-200 text-black"
          } ${isSameSender ? "mt-2" : "mt-8"}`}
        >
          {children}
        </div>
      </div>
    );
  }
  