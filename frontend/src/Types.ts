import React, { SetStateAction } from "react"

interface Company {
    name: string,
    phone: string,
    CNPJ: string
}

export interface UserType {
    first_name: string,
    email: string,
    company: Company | null,
    money: number,
}

export type UserContextType = [UserType|null, React.Dispatch<SetStateAction<UserType|null>>]

export interface JWT {
    refresh: string,
    access: string
}

export type JWTContextType = [JWT|null, React.Dispatch<SetStateAction<JWT|null>>]

export type CSRFType = string

export type CSRFContextType = [CSRFType|null, React.Dispatch<SetStateAction<CSRFType|null>>]
