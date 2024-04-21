import Link from "next/link";

async function getUsers() {
  const response = await fetch('http://localhost:4000/api/flask/most_recent_tournament_with_users')
  .then(res =>  {return res.json()})
  return response;
}

export default async function HomePage() {
  const most_recent_tournament = await getUsers();
  console.log(most_recent_tournament);
  return (
    <main className="">
      <div className="flex "></div>
    </main>
  );
}
