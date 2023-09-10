/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Item } from './Item';

export type UserWithItems = {
    createdAt: string;
    updatedAt?: (string | null);
    id: (number | string);
    email: string;
    password: string;
    active: boolean;
    verified: boolean;
    sudo: boolean;
    twoFactor: boolean;
    firstName?: (string | null);
    lastName?: (string | null);
    dateOfBirth?: (string | null);
    country?: (string | null);
    phoneNumber?: (string | null);
    items: Array<Item>;
};

