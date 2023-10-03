import {
  AddIcon,
  CalendarIcon,
  CheckIcon,
  CloseIcon,
  DownloadIcon,
} from "@chakra-ui/icons";
import {
  Box,
  Button,
  Center,
  Editable,
  EditableInput,
  EditablePreview,
  Flex,
  HStack,
  Icon,
  IconButton,
  Input,
  Link,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Select,
  SimpleGrid,
  Spinner,
  Text,
  useDisclosure,
} from "@chakra-ui/react";
import React, { Dispatch, SetStateAction, useState } from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BsShop } from "react-icons/bs";
import { RiMoneyDollarBoxLine } from "react-icons/ri";
import {
  Categories,
  Receipt,
  ReceiptEntryService,
  ReceiptService,
  Store,
  StoreService,
} from "../../client";

import { ReceiptEntryUpdate } from "../../../../.app2/src/client/models/ReceiptEntryUpdate";
import { useNavigate, useParams } from "react-router-dom";
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
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { id } = useParams();
  console.log(receipt);
  const navigate = useNavigate();
  const receiptID = id || 0;
  const [shop, setShop] = useState(receipt.store?.name);
  const [editShop, setEditShop] = useState(false);

  const [editShopValue, setEditShopValue] = useState(shop);
  const [addShop, setAddShop] = useState(false);
  const [addShopValue, setAddShopValue] = useState("");
  const [editCurrentShop, setEditCurrentShop] = useState(false);
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

  async function handlePatch(type: string, e?: React.FormEvent) {
    if (e) e.preventDefault();
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
    try {
      setIsLoading(true);
      const response = await ReceiptEntryService.receiptEntryUpdateReceiptEntry(
        receiptID,
        payload
      );
      if (response.status === 200) {
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

  async function updateShopInDB() {
    if (!shop) return;
    const storeObjectWithID = stores.find((store) => store.name === shop);
    if (!storeObjectWithID) return;
    try {
      const response = await StoreService.storeUpdateStore(
        storeObjectWithID.id,
        { name: editShopValue }
      );
      setShop(editShopValue);
      update((prev) => !prev);
      setEditShop(false);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleAddStoreToDB() {
    if (!addShopValue) return;

    try {
      const response = await StoreService.storeCreateStore({
        name: addShopValue,
      });
      if (response.status === 201) {
        await handleUpdateStoreID(response.body["id"]);
        update((prev) => !prev);
        setShop(addShopValue);
        setEditShop(false);
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function handleUpdateStoreID(newStoreID: number) {
    try {
      const response = await ReceiptEntryService.receiptEntryUpdateReceiptEntry(
        receiptID,
        { storeId: newStoreID }
      );
    } catch (error) {
      console.error(error);
    }
  }
  async function handleDelete() {
    if (!receiptID) return;
    try {
      const response = await ReceiptService.receiptDeleteSpecificFullReceipt(
        receiptID
      );
      navigate("/receipts");
    } catch (e) {
      console.error(e);
    }
  }
  console.log(stores);
  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Delete Receipt</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            Are you sure you want to delete this receipt? Data will be
            permanently lost!
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="red" mr={3} onClick={handleDelete}>
              Delete
            </Button>
            <Button variant="ghost" onClick={onClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <SimpleGrid columns={2} spacing={10}>
        <Text as="b">
          <Icon as={BsShop} mr="12px" />
          Shop:
        </Text>
        {editShop ? (
          <>
            <Flex as="form" onSubmit={(e) => handlePatch("store", e)}>
              {/* <Box w={80}>
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
            </Box> */}
              <Select
                value={shop}
                size="sm"
                placeholder={"............"}
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
                variant="ghost"
                type="submit"
                size="sm"
                aria-label="edit shop"
                icon={<CheckIcon />}
                mr={1}
              />
              <IconButton
                variant="ghost"
                size="sm"
                aria-label="cancel"
                icon={<CloseIcon />}
                onClick={() => setEditShop(false)}
              />
            </Flex>
            <Button
              variant={addShop ? "outline" : "ghost"}
              onClick={() => {
                setAddShop((prev) => !prev);
                setEditCurrentShop(false);
              }}
            >
              Add shop
            </Button>
            <Button
              variant={editCurrentShop ? "outline" : "ghost"}
              onClick={() => {
                setEditCurrentShop((prev) => !prev);
                setAddShop(false);
              }}
            >
              Edit Shop
            </Button>
            {editCurrentShop && (
              <>
                <Input
                  value={editShopValue}
                  onChange={(e) => setEditShopValue(e.target.value)}
                ></Input>
                <Button
                  leftIcon={<AiOutlineEdit />}
                  type="submit"
                  outline="ghost"
                  onClick={updateShopInDB}
                >
                  Edit
                </Button>{" "}
              </>
            )}
            {addShop && (
              <>
                <Input
                  value={addShopValue}
                  onChange={(e) => setAddShopValue(e.target.value)}
                ></Input>
                <Button
                  leftIcon={<AddIcon />}
                  type="submit"
                  onClick={handleAddStoreToDB}
                >
                  Add
                </Button>{" "}
              </>
            )}
          </>
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
              colorScheme="teal"
              variant="ghost"
              aria-label="edit category"
              icon={<CheckIcon />}
              mr={1}
              ml={1}
            />
            <IconButton
              size="sm"
              variant="ghost"
              colorScheme="teal"
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
          <Flex
            as="form"
            onSubmit={(e) => {
              handlePatch("purchaseDate", e);
              console.log("e is :   ", e);
            }}
          >
            <Input
              size="sm"
              type="date"
              value={purchaseDate}
              onChange={(e) => setPurchaseDate(e.target.value)}
            />
            <IconButton
              mr={1}
              ml={1}
              variant="ghost"
              type="submit"
              size="sm"
              aria-label="edit date"
              icon={<CheckIcon />}
            />
            <IconButton
              variant="ghost"
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
            <Text>{purchaseDate}</Text>
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
              variant="ghost"
              type="submit"
              size="sm"
              aria-label="edit store"
              icon={<CheckIcon />}
              mr={1}
              ml={1}
            />
            <IconButton
              variant="ghost"
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
        {/* <Center> */}
        <Button
          size={"sm"}
          leftIcon={<CloseIcon />}
          colorScheme="red"
          onClick={onOpen}
        >
          delete
        </Button>
        {/* </Center> */}
      </SimpleGrid>
      {isLoading && <Spinner />}
    </>
  );
}
