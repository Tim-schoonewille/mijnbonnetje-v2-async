import {
  CalendarIcon,
  CheckIcon,
  CloseIcon,
  DownloadIcon,
} from "@chakra-ui/icons";
import {
  Button,
  Editable,
  EditableInput,
  EditablePreview,
  Flex,
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
import { Categories, Receipt, ReceiptEntryService, Store } from "../../client";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { ReceiptEntryUpdate } from "../../../../.app2/src/client/models/ReceiptEntryUpdate";
import { useParams } from "react-router-dom";

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

  async function handlePatch(e: React.FormEvent, type: string) {
    e.preventDefault();
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

  return (
    <>
      <SimpleGrid columns={2} spacing={10}>
        <Text as="b">
          <Icon as={BsShop} mr="12px" />
          Shop:
        </Text>
        {editShop ? (
          <Flex as="form" onSubmit={(e) => handlePatch(e, "store")}>
            <Select
              value={shop}
              size="xs"
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
            </Select>
            <IconButton
              type="submit"
              size="xs"
              aria-label="edit shop"
              icon={<CheckIcon />}
            />
            <IconButton
              size="xs"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditShop(false)}
            />
          </Flex>
        ) : (
          <Text onClick={() => setEditShop(true)}>{shop}</Text>
        )}
        <Text as="b">
          <Icon as={BiCategoryAlt} mr="12px" />
          Category:
        </Text>
        {editCategory ? (
          <Flex as="form" onSubmit={(e) => handlePatch(e, "category")}>
            <Select
              value={category}
              size="xs"
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
              size="xs"
              aria-label="edit category"
              icon={<CheckIcon />}
            />
            <IconButton
              size="xs"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditCategory(false)}
            />
          </Flex>
        ) : (
          <Text onClick={() => setEditCategory(true)}>{category}</Text>
        )}
        <Text as="b">
          <Icon as={CalendarIcon} mr="12px" />
          Purchase date:
        </Text>
        {editPurchaseDate ? (
          <Flex as="form" onSubmit={(e) => handlePatch(e, "purchaseDate")}>
            <Input
              size="xs"
              type="date"
              value={purchaseDate}
              onChange={(e) => setPurchaseDate(e.target.value)}
            />
            <IconButton
              type="submit"
              size="xs"
              aria-label="edit date"
              icon={<CheckIcon />}
            />
            <IconButton
              size="xs"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditPurchaseDate(false)}
            />
          </Flex>
        ) : (
          <Text onClick={() => setEditPurchaseDate(true)}>
            {receipt.purchaseDate}
          </Text>
        )}
        <Text as="b">
          <Icon as={RiMoneyDollarBoxLine} mr="12px" />
          Total amount:
        </Text>
        {editTotalAmount ? (
          <Flex as="form" onSubmit={(e) => handlePatch(e, "totalAmount")}>
            <Input
              size="xs"
              value={totalAmount}
              onChange={(e) => setTotalAmount(e.target.value)}
            />
            <IconButton
              type="submit"
              size="xs"
              aria-label="edit store"
              icon={<CheckIcon />}
            />
            <IconButton
              size="xs"
              aria-label="cancel"
              icon={<CloseIcon />}
              onClick={() => setEditTotalAmount(false)}
            />
          </Flex>
        ) : (
          <Text onClick={() => setEditTotalAmount(true)}>{totalAmount}</Text>
        )}
        {/* <Text>€ {receipt.totalAmount ? receipt.totalAmount / 100 : ""}</Text> */}
        <Text as="b">
          <DownloadIcon mr="10px" />
          <Link
            href={`http://backend.mijnbonnetje.lan:8000/${receipt.receiptFiles[0].filePath}`}
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
