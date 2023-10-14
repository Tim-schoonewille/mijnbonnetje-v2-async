import React, { Dispatch, SetStateAction } from "react";
import SingleProductItem from "./SingleProductItem";
import { Flex, Icon, Spinner, Text } from "@chakra-ui/react";

import { MdProductionQuantityLimits } from "react-icons/md";
import { ProductItem } from "../../client";

type ProductItemsProps = {
  productItems: ProductItem[] | undefined | null;
  update: Dispatch<SetStateAction<boolean>>;
};
export default function ProductItems({
  productItems,
  update,
}: ProductItemsProps) {
  if (productItems === null || productItems === undefined)
    //return <Text>Error loading products</Text>;
    return <Spinner />;
  return (
    <>
      <Flex flexDirection="column" gap={3}>
        <Text as="b">
          <Icon as={MdProductionQuantityLimits} mr="9px" /> Product Items
        </Text>
        <Flex flexDirection="column" gap="12px">
          {productItems.map((product) => {
            return (
              <SingleProductItem
                key={product.id}
                product={product}
                update={update}
              />
            );
          })}
        </Flex>
      </Flex>
    </>
  );
}
