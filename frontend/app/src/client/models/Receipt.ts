/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Categories } from './Categories';
import type { ProductItem } from './ProductItem';
import type { ReceiptFile } from './ReceiptFile';
import type { ReceiptScan } from './ReceiptScan';
import type { Store } from './Store';

export type Receipt = {
    createdAt: string;
    updatedAt?: (string | null);
    userId: (number | string);
    id: (number | string);
    storeId?: (number | string | null);
    purchaseDate: string;
    totalAmount?: (number | null);
    warranty: number;
    category: Categories;
    receiptFiles: Array<ReceiptFile>;
    receiptScans: Array<ReceiptScan>;
    store?: (Store | null);
    productItems?: (Array<ProductItem> | null);
};

