// write a function that takes a query string and returns a response from the server

import { NextApiRequest, NextApiResponse } from "next";

const API_HOST = process.env.API_HOST

export default async function (req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "POST") {
        res.status(405).json({ error: 'Method not allowed' });
    } 

    const { query } = req.body;
    console.log("Query:", query);

    let endpoint = "";
    if(query == "getItems") {
        endpoint = "all_vids";
    } else if(query == "deleteItem") {
        endpoint = "del_vid";
    } else if(query == "addItem") {
        endpoint = "add_vid";
    }

    try {
        const response = await fetch(`${API_HOST}/${endpoint}`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(req.body)
        });

        const data = await response.json();
        console.log("Data:", data);
        res.status(200).json(data);
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ error: "Internal server error" });
    }
}
