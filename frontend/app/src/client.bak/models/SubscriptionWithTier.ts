/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Payment } from './Payment';
import type { Tier } from './Tier';

export type SubscriptionWithTier = {
    tierId: (number | string);
    startDate: string;
    endDate: string;
    createdAt: string;
    updatedAt?: (string | null);
    userId: (number | string);
    id: (number | string);
    active: boolean;
    tier: Tier;
    payments: (Array<Payment> | null);
};

