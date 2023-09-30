/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Payment } from '../models/Payment';
import type { PaymentCreateSchema } from '../models/PaymentCreateSchema';
import type { UpdatePayment } from '../models/UpdatePayment';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PaymentService {

    /**
     * Read All Payments
     * Return all payment history.
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns Payment Successful Response
     * @throws ApiError
     */
    public static paymentReadAllPayments(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<Payment>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sub/payment/',
            query: {
                'skip': skip,
                'limit': limit,
                'user_id': userId,
                'start_date': startDate,
                'end_date': endDate,
                'date_filter': dateFilter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Payment
     * Create a new payment for a requested subscription.
     *
     * Raises:
     *
     * 400: {detail: 'PAYMENT_ALREADY_FULFILLED}
     *
     * 402: {detail: 'PAYMENT_PENDING}
     *
     * 403: {detail: 'NO_SUB_OR_NOT_YOUR_SUB'}
     * @param requestBody
     * @returns Payment Successful Response
     * @throws ApiError
     */
    public static paymentCreatePayment(
        requestBody: PaymentCreateSchema,
    ): CancelablePromise<Payment> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sub/payment/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Payment
     * Route to update a payment status.
     *
     * Raises:
     *
     * 400: {detail: 'PAYMENT_COMPLETED_OR_EXPIRED}
     *
     * 404: {detail: 'INVALID_PAYMENT_ID}
     * @param externalId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static paymentUpdatePayment(
        externalId: string,
        requestBody: UpdatePayment,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sub/payment/update',
            query: {
                'external_id': externalId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Pending Payment
     * Returns pending payment(s)
     * @returns any Successful Response
     * @throws ApiError
     */
    public static paymentReadPendingPayment(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sub/payment/pending',
        });
    }

    /**
     * Read Specific Payment
     * Returns data from specific payment.
     *
     * Raises:
     *
     * 404: {detail: 'PAYMENT_NOT_FOUND'}
     * @param paymentId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static paymentReadSpecificPayment(
        paymentId: (number | string),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sub/payment/{payment_id}',
            path: {
                'payment_id': paymentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Payment
     * Delete a payment (requires sudo)
     *
     * Raises:
     *
     * 404: {detail: 'PAYMENT_NOT_FOUND'}
     * @param paymentId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static paymentDeletePayment(
        paymentId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/sub/payment/{payment_id}',
            path: {
                'payment_id': paymentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
