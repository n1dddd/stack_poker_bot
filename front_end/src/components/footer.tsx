import Link from "next/link";

export default function Footer() {
  return (
    <div className="xl:px-0 px-4 flex flex-col w-full self-center pt-24">
        <div className="border-t-2 border-white flex flex-row justify-evenly pt-8">
          <Link href={"/members"}>
            <h1 className="flex text-xl text-stroke font-bold text-center">Members</h1>
          </Link>
          <Link href={"/tournaments"}>
            <h1 className="flex text-xl text-stroke font-bold text-center">Tournaments</h1>
          </Link>
          <Link href={"/about"}>
            <h1 className="flex text-xl text-stroke font-bold text-center">About</h1>
          </Link>
        </div>
        <div className="flex flex-row self-center pt-8">
          <h1 className="flex text-sm text-stroke font-bold text-center">Created By Daniel Seniv</h1>
        </div>
    </div>
  )
}
