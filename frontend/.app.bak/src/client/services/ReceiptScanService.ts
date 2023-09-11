/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ReceiptScan } from '../models/ReceiptScan';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ReceiptScanService {

    /**
     * Create Receipt Scan
     * Creates a new scan of a receipt file.
     * Gets the file, parses it through an OCR image processor.
     * Saves the scan to database.
     *
     * Raises:
     *
     * 404: {detail: "RECEIPT_FILE_NOT_FOUND"}
     * 403: {detail: "ACCESS_DENIED"}
     * 404: {detail: "INVALID_FILE_PATH"}
     * @param receiptFileId
     * @returns ReceiptScan Successful Response
     * @throws ApiError
     */
    public static receiptScanCreateReceiptScan(
        receiptFileId: (number | string),
    ): CancelablePromise<ReceiptScan> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/receipt-scan/',
            query: {
                'receipt_file_id': receiptFileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Multiple Receipt Scans
     * Read multiple receipt scans.
     * With filter parameters.
     * Requires verified user token.
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns ReceiptScan Successful Response
     * @throws ApiError
     */
    public static receiptScanReadMultipleReceiptScans(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<ReceiptScan>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/receipt-scan',
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
     * Read Specific Receipt Scan
     * Read specific receipt scan from database
     * Checks for ownership in the file.
     *
     * Raises:
     * 404: {detail="RECEIPT_SCAN_NOT_FOUND}
     * 403: {detail="ACCESS_DENIED"}
     * @param receiptScanId
     * @returns ReceiptScan Successful Response
     * @throws ApiError
     */
    public static receiptScanReadSpecificReceiptScan(
        receiptScanId: (number | string),
    ): CancelablePromise<ReceiptScan> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/receipt-scan/{receipt_scan_id}',
            path: {
                'receipt_scan_id': receiptScanId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Receipt Scan
     * delete specific receipt scan from database
     * Checks for ownership in the file.
     *
     * Raises:
     * 404: {detail="RECEIPT_SCAN_NOT_FOUND}
     * 403: {detail="ACCESS_DENIED"}
     * @param receiptScanId
     * @returns string Successful Response
     * @throws ApiError
     */
    public static receiptScanDeleteReceiptScan(
        receiptScanId: (number | string),
    ): CancelablePromise<Record<string, string>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/receipt-scan/{receipt_scan_id}',
            path: {
                'receipt_scan_id': receiptScanId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
