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
  Text,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BsShop } from "react-icons/bs";
import { RiMoneyDollarBoxLine } from "react-icons/ri";
import { Categories, Receipt, Store } from "../../client";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

type ReceiptSummaryProps = {
  receipt: Receipt;
  stores: Store[];
};

export default function ReceiptSummary({
  receipt,
  stores,
}: ReceiptSummaryProps) {
  const [shop, setShop] = useState(receipt.store?.name);
  const [editShop, setEditShop] = useState(false);
  const [category, setCategory] = useState(receipt.category);
  const [editCategory, setEditCategory] = useState(false);
  const [purchaseDate, setPurchaseDate] = useState(receipt.purchaseDate);
  const [editPurchaseDate, setEditPurchaseDate] = useState(false);
  const [totalAmount, setTotalAmount] = useState(
    receipt?.totalAmount ? (receipt.totalAmount / 100).toString() : ""
  );
  const [editTotalAmount, setEditTotalAmount] = useState(false);
  const categories = Object.values(Categories);
  if (receipt === null || receipt === undefined)
    return <Text>Error fetching file</Text>;

  return (
    <>
      <SimpleGrid columns={2} spacing={10}>
        <Text as="b">
          <Icon as={BsShop} mr="12px" />
          Shop:
        </Text>
        {editShop ? (
          <Flex>
            <Select size="xs" placeholder={shop}>
              {stores.map((store) => {
                return <option key={store.id}>{store.name}</option>;
              })}
            </Select>
            <IconButton size="xs" aria-label="edit shop" icon={<CheckIcon />} />
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
          <Flex>
            <Select size="xs" placeholder={category}>
              {categories.map((category, i) => {
                return <option key={i}>{category}</option>;
              })}
            </Select>
            <IconButton
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
          <Flex>
            <Input size="xs" type="date" value={purchaseDate} />
            <IconButton size="xs" aria-label="edit date" icon={<CheckIcon />} />
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
          <Flex>
            <Input
              size="xs"
              value={totalAmount}
              onChange={(e) => setTotalAmount(e.target.value)}
            />
            <IconButton
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
    </>
  );
}
