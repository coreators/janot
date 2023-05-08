import type { NextApiRequest, NextApiResponse } from "next";
import { loadAndSearch } from "../../../lib/services/document-service";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  switch (req.method) {
    case "GET":
      handleGet();
      break;

    default:
      res.status(405).json({
        message: "Method not allowed",
      });
      break;
  }

  async function handleGet() {
    const searchResult = await loadAndSearch();

    res.status(200).json(searchResult);
  }
}
