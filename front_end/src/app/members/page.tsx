import MemberList from "~/components/member_list";

export default async function Members() {
  return (
    <main className="2xl:w-3/4 xl:px-0 px-4 w-full flex-col self-center justify-self-center py-8">
      <MemberList />
    </main>
  );
}
