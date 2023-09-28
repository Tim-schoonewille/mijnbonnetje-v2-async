import { AddIcon } from "@chakra-ui/icons";
import { Button, Flex, Heading, Input, Text } from "@chakra-ui/react";
import React, { ChangeEvent, useState } from "react";

export default function AddReceiptPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
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
  return (
    <Flex
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      gap={15}
      mt="24px"
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
        <Button as="span" variant="outline" cursor="pointer">
          Select File
        </Button>
      </label>
      {selectedFile && (
        <>
          <strong>Selected File:</strong> {selectedFile.name}
        </>
      )}
      <Button type="submit" onClick={triggerFileInput}>
        Add Receipt
      </Button>
    </Flex>
  );
}
