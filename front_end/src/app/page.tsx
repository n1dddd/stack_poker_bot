"use client";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function HomePage() {

  useEffect(() => {
    fetch('/api/flask/users')
      .then(res => console.log(res.json()))
  }) 
  return (
    <main className="">
      <div className="flex "></div>
    </main>
  );
}
