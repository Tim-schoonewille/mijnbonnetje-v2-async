import {
  Box,
  Button,
  Editable,
  EditableInput,
  EditablePreview,
  Flex,
  Grid,
  HStack,
  Icon,
  IconButton,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Spacer,
  Text,
  useDisclosure,
} from "@chakra-ui/react";
import React, { Dispatch, SetStateAction, useState } from "react";
import { ProductItem, ProductItemService } from "../../client";
import { AiOutlineCheck, AiOutlineClose, AiOutlineEdit } from "react-icons/ai";
import { CloseIcon } from "@chakra-ui/icons";
import { IoCloseCircleOutline } from "react-icons/io5";

type SingleProductItemProps = {
  product: ProductItem;
  update: Dispatch<SetStateAction<boolean>>;
};

export default function SingleProductItem({
  product,
  update,
}: SingleProductItemProps) {
  const [editItem, setEditItem] = useState(false);
  const [productQuantity, setProductQuantity] = useState(product.quantity);
  const [productName, setProductName] = useState(product.name.toLowerCase());
  const [productPrice, setProductPrice] = useState(product.price);
  const { isOpen, onOpen, onClose } = useDisclosure();

  async function handleProductPatch() {
    console.log("updating....");
    let payload = {};
    if (productQuantity !== product.quantity) {
      console.log("Quantity is different..");
      payload = { ...payload, quantity: productQuantity };
    }
    if (productName !== product.name) {
      console.log("Name is different");
      payload = { ...payload, name: productName };
    }
    if (productPrice !== product.price) {
      console.log("Price is different");
      payload = { ...payload, price: productPrice };
    }
    try {
      const response =
        await ProductItemService.productItemUpdateSpecificProductItem(
          product.id,
          payload
        );
      console.log("upatig priceip");
    } catch (e) {
      console.error(e);
    } finally {
      setEditItem(false);
    }
  }

  async function handleDeleteProductItem() {
    try {
      const response =
        await ProductItemService.productItemDeleteSpecificProductItem(
          product.id
        );
      if (response.status === 200) {
        update((prev) => !prev);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setEditItem(false);
      onClose();
    }
  }
  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader as="i">Delete item..</ModalHeader>
          <ModalCloseButton colorScheme="teal" />
          <ModalBody>
            <Text mb="24px">
              Are you sure you want to delete this product item: {product.name}
            </Text>
            <Text as="b">Data will be permanently lost..!</Text>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="red" mr={3} onClick={handleDeleteProductItem}>
              Delete
            </Button>
            <Button colorScheme="teal" variant="ghost" onClick={onClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      <Button
        width={"100%"}
        variant={editItem ? "link" : "ghost"}
        p={0}
        m={0}
        onClick={() => !editItem && setEditItem(true)}
      >
        <Flex alignItems="center" justifyContent="space-between">
          <Box width="30px" mr={editItem ? 5 : 3}>
            {editItem ? (
              <Input
                type="number"
                value={Number(productQuantity)}
                onChange={(e) => setProductQuantity(Number(e.target.value))}
                size={"sm"}
                mr={4}
                variant="flushed"
              />
            ) : (
              <Text as="i">{productQuantity} </Text>
            )}
          </Box>
          <Box width="180px" mr={editItem ? 5 : 3}>
            {editItem ? (
              <Input
                size="sm"
                type="text"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                variant="flushed"
              />
            ) : (
              <Text as="i">{productName}</Text>
            )}
          </Box>
          <Box width="60px">
            {editItem ? (
              <Input
                size="sm"
                type="number"
                value={Number(productPrice)}
                onChange={(e) => setProductPrice(Number(e.target.value))}
                variant="flushed"
              />
            ) : (
              <Text as="i"> € {productPrice} </Text>
            )}
          </Box>
          {!editItem && (
            <Box>
              <IconButton
                size="xs"
                variant="ghost"
                aria-label="edit product item"
                icon={<AiOutlineEdit />}
                onClick={() => setEditItem(true)}
              />
              <IconButton
                colorScheme="red"
                size="sm"
                variant="ghost"
                aria-label="edit product item"
                icon={<AiOutlineClose />}
                onClick={onOpen}
              />
            </Box>
          )}{" "}
        </Flex>
      </Button>
      {editItem && (
        <HStack ml={"auto"} mr="auto">
          <IconButton
            colorScheme="teal"
            type="submit"
            size="sm"
            variant="ghost"
            aria-label="edit product item"
            icon={<AiOutlineCheck />}
            onClick={handleProductPatch}
          />
          <Button
            size="sm"
            variant="ghost"
            aria-label="edit product item"
            onClick={() => {
              setEditItem(false);
              setProductName(product.name);
              setProductQuantity(product.quantity);
              setProductPrice(product.price);
            }}
          >
            close
          </Button>
          <IconButton
            colorScheme="red"
            size="sm"
            variant="ghost"
            aria-label="edit product item"
            icon={<AiOutlineClose />}
            onClick={onOpen}
          />
        </HStack>
      )}
    </>
    // <Grid templateColumns="60px 450px 80px 30px" gap="10px" alignItems="center">
    //   <Text as="i">{product.quantity} x</Text>
    //   <Text as="i">{product.name.toLowerCase()}</Text>
    //   <Text as="i">€ {product.price}</Text>
    //   <Icon as={AiOutlineEdit} />
    // </Grid>
  );
}
