/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Categories } from './Categories';

export type ReceiptEntry = {
    createdAt: string;
    updatedAt?: (string | null);
    userId: (number | string);
    id: (number | string);
    storeId?: (number | string | null);
    purchaseDate: string;
    totalAmount?: (number | null);
    warranty: number;
    category: Categories;
};

