import { ArrowRight, Search } from "lucide-react";
import Head from "next/head";
import Link from "next/link";
import { useState } from "react";
import PromptForm from "~/components/promptform";

export default function Home() {

  return (
    <>
      <Head>
        <title>Video Search</title>
        <meta name="description" content="Search your video collection" />
        <link rel="icon" href="/search.png" />
      </Head>
      <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c]">
        <h1 className="text-4xl text-white">Video Search</h1>
        
        <Link className="bg-white text-black rounded-md p-3 mt-8 flex items-center" href={"/chat"}>
          Search your video collection
          <div className="ml-2 bg-black text-white p-2 rounded-full">
            <ArrowRight/>
          </div>
        </Link>
      </main>
    </>
  );
}
