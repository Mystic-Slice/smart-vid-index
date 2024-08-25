import { ArrowRight, Search } from "lucide-react";
import Head from "next/head";
import Link from "next/link";
import { useState } from "react";
import PromptForm from "~/components/promptform";

export default function Home() {

  return (
    <>
      <Head>
        <title>Smart Video Index</title>
        <meta name="description" content="Search your video collection" />
        <link rel="icon" href="/search.png" />
      </Head>
      <main className="flex min-h-screen flex-col items-center justify-center bg-my-white">
        <div className="p-10 rounded-xl w-1/2 h-1/2 flex flex-col justify-center">
          <h1 className="text-4xl text-center text-black font-serif">Smart Video Index</h1>
        
          <Link className="w-1/2 rounded-md p-3 mt-8 m-auto flex items-center justify-center" href={"/chat"}>
            Search your video collection
            <div className="ml-2 border-my-accent border-2 text-background-color p-2 rounded-full">
              <ArrowRight/>
            </div>
          </Link>
        </div>
        
      </main>
    </>
  );
}
