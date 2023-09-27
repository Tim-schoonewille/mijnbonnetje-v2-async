/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PaymentStatus } from './PaymentStatus';

export type Payment = {
    createdAt: string;
    updatedAt?: (string | null);
    subscriptionId: (number | string);
    userId: (number | string);
    id: (number | string);
    paymentDate?: (string | null);
    externalId: string;
    amount: number;
    method?: (string | null);
    status: PaymentStatus;
};

