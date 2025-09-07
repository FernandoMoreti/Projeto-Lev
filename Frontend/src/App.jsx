import React, { useState } from 'react'
import './App.css'
import logo from "../public/logo.jpg"

function App() {

  const [file, setFile] = useState("")
  const [banco, setBanco] = useState("")
  
  async function handleSubmit(e) {
    e.preventDefault()

    const formData = new FormData();
    formData.append("banco", banco)
    formData.append("arquivo", file)

    for (let [key, value] of formData.entries()) {
      console.log(key, value);
    }
    
    const response = await fetch("http://127.0.0.1:5000/executar", {
      method: "POST",
      body: formData,
    })

    const data = await response.json();
    console.log(data.resultado)
  }

  const bancos = [
    "amigoz",
    "brb360",
    "bv",
    "c6vista",
    "grandino",
    "happy",
    "queromais"
  ]

  return (
    <>
      <section className='flex justify-center items-center h-screen bg-gradient-to-tr from-black to-purple-500'>
        <div className='flex bg-black/10 rounded-4xl shadow-2xl shadow-gray-700'>
          <div className='flex flex-col p-10 w-120'>
            <h1 className='flex justify-center text-xl font-semibold'>Bem vindo ao Conversor WORKBANK</h1>
            <form onSubmit={handleSubmit} className='flex flex-col gap-5' action="">
              <p className='text-lg pt-5'>Importe o relatorio:</p>
              <input className="border rounded-xl p-5 shadow-xl shadow-gray-700 cursor-pointer" onChange={(e) => setFile(e.target.files[0])} type="file" />
              <p className='text-lg'>Escolha o banco:</p>
              <select onChange={(e) => {setBanco(e.target.value)}} className='border rounded-xl p-5 shadow-xl shadow-gray-700 cursor-pointer' name="Banco" id="">
                {bancos.map((banco) => (
                  <option className='bg-black' value={banco}>{banco}</option>
                ))}
              </select>
              <button className='border rounded-xl p-5 shadow-xl shadow-gray-700 transition-all durarion-400 cursor-pointer hover:bg-gray-300 hover:text-black' type='submit'>Criar arquivo</button>
            </form>
          </div>
          <img className='w-120 rounded-r-4xl' src={logo} alt="" />
        </div>
      </section>

    </>
  )
}

export default App
