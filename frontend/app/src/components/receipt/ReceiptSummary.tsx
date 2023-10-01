import {
  CalendarIcon,
  CheckIcon,
  CloseIcon,
  DownloadIcon,
} from "@chakra-ui/icons";
import {
  Box,
  Button,
  Editable,
  EditableInput,
  EditablePreview,
  Flex,
  HStack,
  Icon,
  IconButton,
  Input,
  Link,
  Select,
  SimpleGrid,
  Spinner,
  Text,
} from "@chakra-ui/react";
import React, { Dispatch, SetStateAction, useState } from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BsShop } from "react-icons/bs";
import { RiMoneyDollarBoxLine } from "react-icons/ri";
import {
  Categories,
  Receipt,
  ReceiptEntryService,
  Store,
  StoreService,
} from "../../client";

import { ReceiptEntryUpdate } from "../../../../.app2/src/client/models/ReceiptEntryUpdate";
import { useParams } from "react-router-dom";
import { AiOutlineEdit } from "react-icons/ai";
import { LiaHandMiddleFingerSolid } from "react-icons/lia";
import { CreatableSelect } from "chakra-react-select";
type ReceiptSummaryProps = {
  receipt: Receipt;
  stores: Store[];
  update: Dispatch<SetStateAction<boolean>>;
};

export default function ReceiptSummary({
  receipt,
  stores,
  update,
}: ReceiptSummaryProps) {
  const { id } = useParams();
  const receiptID = id || 0;
  const [shop, setShop] = useState(receipt.store?.name);
  const [editShop, setEditShop] = useState(false);
  const [category, setCategory] = useState<string | Categories>(
    receipt.category
  );
  const [editCategory, setEditCategory] = useState(false);
  const [purchaseDate, setPurchaseDate] = useState(receipt.purchaseDate);
  const [editPurchaseDate, setEditPurchaseDate] = useState(false);
  const [totalAmount, setTotalAmount] = useState(
    receipt?.totalAmount ? (receipt.totalAmount / 100).toString() : ""
  );
  const [editTotalAmount, setEditTotalAmount] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const categories = Object.values(Categories);
  if (receipt === null || receipt === undefined)
    return <Text>Error fetching file</Text>;

  console.log(purchaseDate);

  async function handlePatch(type: string, e?: React.FormEvent) {
    if(e) e.preventDefault();
    let payload: ReceiptEntryUpdate = {};
    switch (type) {
      case "store":
        const storeWithId = stores.find((store) => store.name === shop);
        if (!storeWithId) break;
        payload = { storeId: storeWithId.id };
        break;
      case "category":
        payload = { category: category };
        break;
      case "purchaseDate":
        payload = { purchaseDate: purchaseDate };
        break;
      case "totalAmount":
        payload = { totalAmount: Number(totalAmount) * 100 };
        break;
      default:
        console.error("not allowed");
    }
    console.log("updating.....");
    try {
      setIsLoading(true);
      const response = await ReceiptEntryService.receiptEntryUpdateReceiptEntry(
        receiptID,
        payload
      );
      if (response.status === 200) {
        console.log("updated!");
        setEditShop(false);
        setEditCategory(false);
        setEditPurchaseDate(false);
        setEditTotalAmount(false);
        update(true);
      } else {
        alert("weeeh");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }

  async function createNewStore(name: string) {
    try {
      const response = await StoreService.storeCreateStore({ name: name });
      console.log(response)
      update(true);
    } catch (e) {
      console.error(e);
    }
  }
  console.log(stores)
  return (
    <>
      <SimpleGrid columns={2} spacing={10}>
        <Text as="b">
          <Icon as={BsShop} mr="12px" />
          Shop:
        </Text>
        {editShop ? (
          <Flex as="form" onSubmit={(e) => handlePatch("store", e)}>
            <Box w={80}>
              <CreatableSelect
                onCreateOption={(e) => {
                  createNewStore(e);
                  handlePatch("store")
                }}
                size={"sm"}
                name="colors"
                options={stores.map((store) => {
                  return { label: store.name, value: store.name };
                })}
                placeholder="select store"
                closeMenuOnSelect={false}
                onChange={(item) => {
                  if (!item) return;
                  setShop(item.value);
                }}
                value={{ label: shop, value: shop }}
              />
            </Box>
            {/* <Select
              value={shop}
              size="sm"
              placeholder={shop}
              onChange={(e) => {
                setShop(e.target.value);
              }}
            >
              {stores.map((store) => {
                return (
                  <option value={store.name} key={store.id}>
                    {store.name}
                  </option>
                );
              })}
            </Select> */}
            <IconButton
              type="submit"
              size="sm"
              aria-label="edit shop"
              icon={<CheckIcon />}
            />
            <IconButton
              size="sm"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditShop(false)}
            />
          </Flex>
        ) : (
          <HStack
            justifyContent={"space-between"}
            onClick={() => setEditShop(true)}
            _hover={{ cursor: "pointer" }}
          >
            <Text>{shop}</Text>
            <Icon as={AiOutlineEdit} />
          </HStack>
        )}
        <Text as="b">
          <Icon as={BiCategoryAlt} mr="12px" />
          Category:
        </Text>
        {editCategory ? (
          <Flex as="form" onSubmit={(e) => handlePatch("category", e)}>
            <Select
              value={category}
              size="sm"
              placeholder={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              {categories.map((category, i) => {
                return (
                  <option value={category} key={i}>
                    {category}
                  </option>
                );
              })}
            </Select>
            <IconButton
              type="submit"
              size="sm"
              aria-label="edit category"
              icon={<CheckIcon />}
            />
            <IconButton
              size="sm"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditCategory(false)}
            />
          </Flex>
        ) : (
          <HStack
            justifyContent={"space-between"}
            onClick={() => setEditCategory(true)}
            _hover={{ cursor: "pointer" }}
          >
            <Text>{category}</Text>
            <Icon as={AiOutlineEdit} />
          </HStack>
        )}
        <Text as="b">
          <Icon as={CalendarIcon} mr="12px" />
          Purchase date:
        </Text>
        {editPurchaseDate ? (
          <Flex as="form" onSubmit={(e) => handlePatch("purchaseDate", e)}>
            <Input
              size="sm"
              type="date"
              value={purchaseDate}
              onChange={(e) => setPurchaseDate(e.target.value)}
            />
            <IconButton
              type="submit"
              size="sm"
              aria-label="edit date"
              icon={<CheckIcon />}
            />
            <IconButton
              size="sm"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditPurchaseDate(false)}
            />
          </Flex>
        ) : (
          <HStack
            justifyContent={"space-between"}
            onClick={() => setEditPurchaseDate(true)}
            _hover={{ cursor: "pointer" }}
          >
            <Text>{receipt.purchaseDate}</Text>
            <Icon as={AiOutlineEdit} />
          </HStack>
        )}
        <Text as="b">
          <Icon as={RiMoneyDollarBoxLine} mr="12px" />
          Total amount:
        </Text>
        {editTotalAmount ? (
          <Flex as="form" onSubmit={(e) => handlePatch("totalAmount", e)}>
            <Input
              size="sm"
              value={totalAmount}
              onChange={(e) => setTotalAmount(e.target.value)}
            />
            <IconButton
              type="submit"
              size="sm"
              aria-label="edit store"
              icon={<CheckIcon />}
            />
            <IconButton
              size="sm"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditTotalAmount(false)}
            />
          </Flex>
        ) : (
          <HStack
            justifyContent={"space-between"}
            onClick={() => setEditTotalAmount(true)}
            _hover={{ cursor: "pointer" }}
          >
            <Text>€ {totalAmount}</Text>
            <Icon as={LiaHandMiddleFingerSolid} />
          </HStack>
        )}
        {/* <Text>€ {receipt.totalAmount ? receipt.totalAmount / 100 : ""}</Text> */}
        <Text as="b">
          <DownloadIcon mr="10px" />
          <Link
            href={`http://frontend.mijnbonnetje.lan:8000/${receipt.receiptFiles[0].filePath}`}
            isExternal
          >
            Download
          </Link>
        </Text>
      </SimpleGrid>
      {isLoading && <Spinner />}
    </>
  );
}
