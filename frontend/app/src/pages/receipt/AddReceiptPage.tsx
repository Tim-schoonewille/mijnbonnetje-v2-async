import { AddIcon } from "@chakra-ui/icons";
import { Button, Flex, Heading, Input, Spinner, Text } from "@chakra-ui/react";
import React, { ChangeEvent, FormEvent, useState } from "react";
import RequiresValidToken from "../../wrappers/RequiresValidToken";
import { Body_receipt_create_full_receipt, ReceiptService } from "../../client";
import { useNavigate } from "react-router-dom";

export default function AddReceiptPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  // Function to handle file selection
  const handleFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    setSelectedFile(file || null);
  };

  // Function to trigger the file input
  const triggerFileInput = () => {
    const fileInput = document.getElementById("fileInput");
    if (fileInput) {
      fileInput.click();
    }
  };
  async function handleNewReceipt() {
    console.log("adding file");
    if (!selectedFile) return;
    const formData: Body_receipt_create_full_receipt = { file: selectedFile };
    const includeExternalOcr = true;

    try {
      setIsLoading(true);
      const response = await ReceiptService.receiptCreateFullReceipt(
        formData,
        includeExternalOcr
      );
      if (response.status === 201) {
        setSuccessMessage("File uploaded!");
        setErrorMessage("");
        navigate(`/receipts/${response.body["id"]}`);
      } else {
        setErrorMessage("Something went wrong. Contact admin");
        setSuccessMessage("");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }
  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!selectedFile) return;
    handleNewReceipt();
  }
  return (
    <RequiresValidToken>
      <Flex
        as="form"
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        gap={15}
        mt="24px"
        onSubmit={handleSubmit}
      >
        <Flex justifyContent={"center"} alignItems={"center"} gap={3}>
          <Text>Add Receipt</Text>
        </Flex>
        <Input
          type="file"
          display="none"
          id="fileInput"
          onChange={handleFileSelect}
        />

        <label htmlFor="fileInput">
          <Button
            colorScheme="teal"
            as="span"
            variant="outline"
            cursor="pointer"
          >
            Select File
          </Button>
        </label>
        {selectedFile && (
          <>
            <strong>Selected File:</strong> {selectedFile.name}
          </>
        )}
        <Button type="submit" colorScheme="teal">
          Add Receipt
        </Button>
        {isLoading && <Spinner />}
        {successMessage && <Text color={"green.400"}> {successMessage}</Text>}
        {errorMessage && <Text color={"red.400"}>{errorMessage}</Text>}
      </Flex>
    </RequiresValidToken>
  );
}
