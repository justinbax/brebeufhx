'use client'
import {useState} from 'react'
import { Recipient, UserPlaceholders } from '@/app/helpers/User'


export default function Send() {
    let nextArrID = 0
    const [template, setTemplate] = useState("")
    const [arrOfRecipients, setArrOfRecipients]: [Array<Recipient>, any] = useState([new Recipient('', '', '')])
    const [arrOfPlaceholders, setArrOfPlaceholders]: [Array<string>, any] = useState([''])
    const [arrOfUserPlaceholders, setArrOfUserPlaceholders]: [Array<UserPlaceholders>, any] = useState([{'': ''}])
    
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

    function handleUpdateUserPlaceHolders(userPlaceHolderObject: UserPlaceholders, key: keyof UserPlaceholders, value: string) {
        let newObj = userPlaceHolderObject
        newObj[key] = value
        return newObj
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
                        onClick={() => {setArrOfRecipients([...arrOfRecipients, new Recipient('', '', '')]); console.log(arrOfRecipients)}}
                        >Add Recipient</button>
                    </div>

                </div>
                <div className="my-2 bg-slate-100 min-h-60 p-8">
                    {
                        Array.from({length: arrOfPlaceholders.length}, (_, i) => (
                            <div key={i} className="grid grid-cols-3 gap-2">
                                <div>
                                <div>Placeholder {`<<`}{arrOfPlaceholders[i]}{`>>`}</div>
                                <input type="text" value={arrOfPlaceholders[i]} onChange={e => handleUpdatePlaceholders(i, e.target.value)} />
                                </div>
                                <div className="grid grid-cols-3 col-span-2">
                                    <PlaceholderPerUser placeholderName={arrOfPlaceholders[i]}></PlaceholderPerUser>
                                </div>

                            </div>
                        ))
                    }
                    <div className="my-2">
                        <button className="bg-yellow-400 p-4 hover:bg-yellow-200" 
                        onClick={() => {setArrOfPlaceholders([...arrOfPlaceholders, '']); console.log(arrOfPlaceholders)}}
                        >Add Recipient</button>
                    </div>
                    
                </div>
                <div className="my-2 bg-slate-100 min-h-60 p-8 grid grid-cols-1">
                    Template here: <br/>
                    <textarea onChange={(e) => setTemplate(e.target.value)}></textarea>
                </div>
                <div className="my-2"><button className="bg-yellow-400 p-4 hover:bg-yellow-200">Submit</button></div>
            </div>
            <div>{template}</div>
            
        </main>
    )
    function PlaceholderPerUser(props:any) {

        return Array.from({length: arrOfRecipients.length}, (_, j) => (
            <div key={j} >
                <input key={j} type="text" value={arrOfRecipients[j].placeholders[props.placeholderName]} onChange={e => handleUpdateRecipientProp(j, "placeholders", handleUpdateUserPlaceHolders(arrOfRecipients[j].placeholders, props.placeholderName, e.target.value))}/> 
            </div>
        ))
    }
}

