import { RaRecord, Identifier } from 'react-admin';
export interface Customer extends RaRecord {
    first_name: string;
    last_name: string;
    address: string;
    stateAbbr: string;
    city: string;
    zipcode: string;
    avatar: string;
    birthday: string;
    first_seen: string;
    last_seen: string;
    has_ordered: boolean;
    latest_purchase: string;
    has_newsletter: boolean;
    groups: string[];
    nb_commands: number;
    total_spent: number;
}

export type OrderStatus = 'ordered' | 'delivered' | 'cancelled';

export interface Order extends RaRecord {
    status: OrderStatus;
    basket: BasketItem[];
    date: Date;
    total: number;
}
export interface BasketItem {
    product_id: Identifier;
    quantity: number;
}
export interface User extends RaRecord {
    id: Identifier;
    email: string;
    first_name: string;
    last_name: string;
    address: string;
    is_active: boolean;
    is_superuser: boolean;
}

export interface Rooms extends RaRecord {
    id: Identifier;
    parent_name: string;
    parent_id: number;
    type_room: number;
    name: string;
    order_sequence: string;
}

declare global {
    interface Window {
        restServer: any;
    }
}
