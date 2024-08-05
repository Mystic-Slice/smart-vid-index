export const apiReq = (apiPath: string, body: any) => {
    return fetch(`/api/${apiPath}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then(t => t.json())
}