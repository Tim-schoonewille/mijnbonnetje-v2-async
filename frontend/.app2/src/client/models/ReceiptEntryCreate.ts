/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Categories } from './Categories';

export type ReceiptEntryCreate = {
    storeId?: (number | string | null);
    purchaseDate?: string;
    totalAmount?: number;
    warranty?: number;
    category?: Categories;
};

