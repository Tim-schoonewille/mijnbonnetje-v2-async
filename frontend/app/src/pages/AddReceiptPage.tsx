import { Checkbox, Flex, Heading, useToast } from "@chakra-ui/react";
import {
  ChakraProvider,
  Box,
  FormControl,
  FormLabel,
  Input,
  Button,
} from "@chakra-ui/react";
import React, { FormEvent, useState } from "react";
import RequiresValidToken from "../wrappers/RequiresValidToken";
import { Body_receipt_create_full_receipt, ReceiptService } from "../client";
import { useNavigate } from "react-router-dom";

export default function AddReceiptPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const toast = useToast();
  const navigate = useNavigate();
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0];
    setSelectedFile(file || null);
  };
  const [useExternalApi, setUseExternalApi] = useState(false);

  const handleNewReceipt = async () => {
    if (!selectedFile) return;

    const formData: Body_receipt_create_full_receipt = { file: selectedFile };
    try {
      const response = await ReceiptService.receiptCreateFullReceipt(
        formData,
        useExternalApi
      );
      if (response.status === 201) {
        console.log("Succesfull uplod!");
        const newReceiptId = response.body["id"];
        console.log(newReceiptId);
        toast({
          title: "Receipt added!",
          description: "New receipt added, you will be forwarded automatically",
          status: "success",
          duration: 4000,
          isClosable: true,
        });
        navigate(`/receipts/${newReceiptId}`);
      }
      console.log(response);
      if (response.status >= 400) {
        console.error("file upload failed");
      }
    } catch (e) {
      console.error(e);
    }
  };
  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    // Handle file upload here using 'selectedFile'
    // You can use FormData to send the file to your server, for example.
    if (selectedFile) {
      // Handle the file upload logic here
      handleNewReceipt();
    }
  };
  return (
    <RequiresValidToken>
      <Flex
        flexDirection={"column"}
        alignItems="center"
        justifyContent="center"
        m="0 auto"
        maxW={400}
        height="80vh"
      >
        <Heading>Add a receipt</Heading>
        <Box p={4}>
          <form onSubmit={handleSubmit}>
            <FormControl>
              <FormLabel htmlFor="file">Choose a file:</FormLabel>
              <Input
                type="file"
                id="file"
                accept=".jpg, .jpeg, .png, .pdf" // Specify the accepted file types
                onChange={handleFileChange}
              />
            </FormControl>
            <Checkbox
              isChecked={useExternalApi}
              m={6}
              onChange={(e) => setUseExternalApi(e.target.checked)}
            >
              Use external api
            </Checkbox>

            <Button type="submit" mt={4} colorScheme="blue">
              Upload File
            </Button>
          </form>
        </Box>
      </Flex>
    </RequiresValidToken>
  );
}
