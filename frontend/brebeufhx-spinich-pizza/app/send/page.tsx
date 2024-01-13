'use client'
import {useState} from 'react'
import { Recipient, UserPlaceholders } from '@/app/helpers/User'


export default function Send() {
    let nextArrID = 0
    const [templateType, setTemplateType] = useState("")
    const [arrOfRecipients, setArrOfRecipients]: [Array<Recipient>, any] = useState([new Recipient('', '', '')])
    const [arrOfPlaceholders, setArrOfPlaceholders]: [Array<string>, any] = useState([''])
    const [arrOfUserPlaceholders, setArrOfUserPlaceholders]: [Array<UserPlaceholders>, any] = useState([{'': ''}])
    
    const axios = require('axios')
    async function doPostRequest(payload: any) {
        let res = await axios.post("/send", payload)
        let data = res.data
        console.log(data)
    }

    function handleUpdateRecipientProp(index: number, prop: keyof Recipient, updatedValue: any) {
        const newArr = arrOfRecipients.map((recipient, i) => {
            if (i === index) {
                let updatedRecipient = recipient
                updatedRecipient[prop] = updatedValue
                return updatedRecipient
            }
            else {
                return recipient
            }
    
        } )
        setArrOfRecipients(newArr)
    }
    
    function handleUpdatePlaceholders(index: number, updatedValue: string) {
        const newArr = arrOfPlaceholders.map((placeholder, i) => {
            if (i === index) {
                return updatedValue
            }
            else {
                return placeholder
            }
    
        } )
        setArrOfPlaceholders(newArr)
    }

    function handleUpdateUserPlaceHolders(index: number, prop: keyof UserPlaceholders, updatedValue: any) {
        const newArr = arrOfUserPlaceholders.map((placeholder, i) => {
            if (i === index) {
                let newPlaceholder = placeholder
                newPlaceholder[prop] = updatedValue
                return newPlaceholder
            }
            else {
                return placeholder
            }
    
        } )
        setArrOfUserPlaceholders(newArr)

    }
    
    function submit() {
        for (let i: number = 0; i < arrOfRecipients.length; i++) {
            handleUpdateRecipientProp(i, 'placeholders', arrOfUserPlaceholders[i])
        }

        doPostRequest({recipients: arrOfRecipients, own_email: "cai.lucia04@gmail.com", type: templateType})
    }
    return (
        <main>
            <div className="grid grid-cols-1 m-12">
                <div className="my-2 text-3xl text-left min-h-40 flex p-8"> <span className="my-auto">Send a new set of emails</span></div>
                <div className="my-2 bg-slate-100 min-h-60 p-8">
                    <div className="grid grid-cols-3 gap-2">
                        <div>First Name</div>
                        <div>Last Name</div>
                        <div>Email</div>    
                    </div>
                    {
                        Array.from({length: arrOfRecipients.length}, (_, i) => (
                            <div key={i} className="my-2 grid grid-cols-3 gap-2">
                                <input type="text" value={arrOfRecipients[i].first_name} onChange={e => handleUpdateRecipientProp(i, "first_name", e.target.value)}/>
                                <input type="text" value={arrOfRecipients[i].last_name} onChange={e => handleUpdateRecipientProp(i, "last_name", e.target.value)}/>
                                <input type="text" value={arrOfRecipients[i].email} onChange={e => handleUpdateRecipientProp(i, "email", e.target.value)}/>
                            </div>
                        ))
                    }
                    <div className="my-2">
                        <button className="bg-yellow-400 p-4 hover:bg-yellow-200" 
                        onClick={() => {setArrOfRecipients([...arrOfRecipients, new Recipient('', '', '')]); setArrOfUserPlaceholders([...arrOfUserPlaceholders, {'': ''}]);console.log(arrOfRecipients)}}
                        >Add Recipient</button>
                    </div>

                </div>
                <div className="my-2 bg-slate-100 min-h-60 p-8">
                    {
                        Array.from({length: arrOfPlaceholders.length}, (_, i) => {
                            
                            return (<div key={i} className="grid grid-cols-3 gap-2">
                                <div>
                                <div>Placeholder {`<<`}{arrOfPlaceholders[i]}{`>>`}</div>
                                <input type="text" value={arrOfPlaceholders[i]} onChange={e => handleUpdatePlaceholders(i, e.target.value)} />
                                </div>
                                <div className="grid grid-cols-3 col-span-2">
                                    {
                                        Array.from({length: arrOfRecipients.length}, (_, j) => (
                                            <div key={j} >
                                            <input key={j} type="text" value={arrOfUserPlaceholders[j][arrOfPlaceholders[i]]} onChange={e => handleUpdateUserPlaceHolders(j, arrOfPlaceholders[i], e.target.value)} /> 
                                            </div>
                            
                                        ))
                                    }
                                </div>

                            </div>)
                        })
                    }
                    <div className="my-2">
                        <button className="bg-yellow-400 p-4 hover:bg-yellow-200" 
                        onClick={() => {setArrOfPlaceholders([...arrOfPlaceholders, '']); console.log(arrOfPlaceholders)}}
                        >Add Recipient</button>
                    </div>
                    
                </div>
                <div className="my-2 bg-slate-100 min-h-60 p-8 grid grid-cols-1">
                    Template type helpers: <br/>
                    <input type="text" value={templateType} onChange={(e) => setTemplateType(e.target.value)}/>
                </div>
                <div className="my-2"><button className="bg-yellow-400 p-4 hover:bg-yellow-200" onClick={() => submit()}>Submit</button></div>
            </div>
            <div>{templateType}</div>
            
        </main>
    )

}

