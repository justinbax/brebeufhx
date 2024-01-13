'use client'
import {useState} from 'react'

export default function Template() {

    const [template, setTemplate] = useState("")
    const [type, setType] = useState("")
    const axios = require('axios')
    async function doPostRequest(payload: any) {
        let res = await axios.post("localhost:3000/template", payload)
        let data = res.data
        console.log(res)
    }

    function submit() {
        doPostRequest({template: template, type: type})
    }

    return (
        <main>
            <div className="grid grid-cols-1 m-12">
                <div className="my-2 bg-slate-100 min-h-60 p-8 grid grid-cols-1 rounded-lg">
                    Template type name: <br/>
                    <input type="text" value={type} onChange={(e) => setType(e.target.value)}/>
                    Template editor: <br/>
                    <textarea onChange={(e) => setTemplate(e.target.value)}/>
                </div>
                <div className="my-2"><button className="bg-yellow-400 p-4 hover:bg-yellow-200" onClick={() => submit()}>Submit</button></div>
            </div>
        </main>
    )
}