export class Recipient {
    first_name?: string
    last_name?: string
    email?: string
    placeholders: UserPlaceholders = {"": ""}
    constructor(fname?:string, lname?:string, email?:string) {
        this.first_name = fname
        this.last_name = lname
        this.email = email
    }
}
export type UserPlaceholders = {[id: string]: string}
