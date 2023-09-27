import React, { useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { Receipt, ReceiptService } from "../client";
import { Box, Text, Stack, Heading, Divider, Link } from "@chakra-ui/react";

export default function SingleReceiptPage() {
  const { id } = useParams();
  const [receipt, setReceipt] = useState<Receipt>();
  const [error, setError] = useState("");

  const getSingleReceipt = async () => {
    const receiptID = id || 0;
    try {
      const response = await ReceiptService.receiptReadSpecificFullReceipt(
        receiptID
      );

      if (response.status === 200) {
        setReceipt(response.body);
      } else {
        setError("error requesting file");
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    getSingleReceipt();
  }, []);

  const firstReceiptFile = receipt?.receiptFiles[0];
  const firstReceiptScan = receipt?.receiptScans[0];
  console.log(receipt);
  return (
    <>
      {error ? (
        error
      ) : (
        <Box p={4} borderWidth="1px" borderRadius="md" boxShadow="md" m={12}>
          <Heading size="md">Receipt Information</Heading>
          <Divider my={2} />
          <Stack spacing={2}>
            <Text>
              <strong>Created At:</strong> {receipt?.createdAt}
            </Text>
            <Text>
              <strong>Updated At:</strong> {receipt?.updatedAt}
            </Text>
            <Text>
              <strong>User ID:</strong> {receipt?.userId}
            </Text>
            <Text>
              <strong>ID:</strong> {receipt?.id}
            </Text>
            <Text>
              <strong>Store ID:</strong> {receipt?.storeId}
            </Text>
            <Text>
              <strong>Purchase Date:</strong> {receipt?.purchaseDate}
            </Text>
            <Text>
              <strong>Total Amount:</strong>€{" "}
              {receipt?.totalAmount ? receipt.totalAmount / 100 : "N/a"}
            </Text>
            <Text>
              <strong>Warranty:</strong> {receipt?.warranty}
            </Text>
            <Text>
              <strong>Category:</strong> {receipt?.category}
            </Text>
          </Stack>
          <Divider my={2} />
          <Heading size="md">Receipt File</Heading>
          <Divider my={2} />
          <Stack spacing={2}>
            <Text>
              <strong>File Name:</strong> {firstReceiptFile?.fileName}
            </Text>
            <Text>
              <strong>File IMAGE:</strong>{" "}
              <Link color={'teal.600'}
                href={`http://backend.mijnbonnetje.lan:8000${firstReceiptFile?.filePath.slice(
                  1
                )}`}
              >
                Click here
              </Link>
            </Text>
            <Text>
              <strong>File Path:</strong> {firstReceiptFile?.filePath}
            </Text>
            <Text>
              <strong>File Type:</strong> {firstReceiptFile?.fileType}
            </Text>
            <Text>
              <strong>File Size:</strong> {firstReceiptFile?.fileSize}
            </Text>
          </Stack>
          <Divider my={2} />
          <Heading size="md">Receipt Scan</Heading>
          <Divider my={2} />
          <Stack spacing={2}>{/* ... Previous fields ... */}</Stack>
          <Divider my={2} />
          <Heading size="md">Store Information</Heading>
          <Divider my={2} />
          <Stack spacing={2}>
            <Text>
              <strong>Store Name:</strong> {receipt?.store?.name}
            </Text>
            <Text>
              <strong>City:</strong> {receipt?.store?.city}
            </Text>
            <Text>
              <strong>Country:</strong> {receipt?.store?.country}
            </Text>
          </Stack>
          <Divider my={2} />
          <Heading size="md">Product Items</Heading>
          <Divider my={2} />
          {receipt?.productItems?.map((item, index) => (
            <Box key={index} borderWidth="1px" borderRadius="md" p={2}>
              <Text>
                <strong>Product {index + 1}:</strong>
              </Text>
              <Stack spacing={2}>
                <Text>
                  <strong>Name:</strong> {item.name}
                </Text>
                <Text>
                  <strong>Price:</strong> ${item.price}
                </Text>
                <Text>
                  <strong>Quantity:</strong> {item.quantity}
                </Text>
                {/* Add more fields as needed */}
              </Stack>
            </Box>
          ))}
        </Box>
      )}
    </>
  );
}
