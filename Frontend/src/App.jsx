import React, { useState } from 'react'
import './App.css'
import logo from "../public/logo.jpg"

function App() {

  const [file, setFile] = useState("")
  const [banco, setBanco] = useState("")
  const [loading, setLoading] = useState(false)
  
  async function handleSubmit(e) {
    e.preventDefault()

    setLoading(true)

    const formData = new FormData();
    formData.append("banco", banco)
    formData.append("arquivo", file)

    try {
      const response = await fetch("http://127.0.0.1:5000/executar", {
        method: "POST",
        body: formData,
      })
  
      const data = await response.json();
      console.log(data.resultado)
    } catch(error) {
      console.error("Erro ao enviar:", error)
    } finally {
      setLoading(false)
    }
    
  }

  const cbancos_ = [
    "agibank",
    "aki capital",
    "amigoz",
<<<<<<< HEAD
    "presenca"
  ]
=======
    "ayude",
    "banrisul",
    "bmg",
    "brb",
    "btw",
    "bv",
    "c6 auto",
    "c6 bank",
    "c6 car equity",
    "cba - caixa",
    "ccb",
    "cetelem",
    "comissão zero",
    "creditas",
    "crefaz",
    "crefisa",
    "daycoval",
    "digio",
    "dryve",
    "edições",
    "euro 17",
    "evol",
    "facta",
    "fit - santander",
    "futuroprev",
    "grandino",
    "happy - teddy",
    "hope",
    "icred",
    "inbursa - teddy",
    "itau",
    "itau 360",
    "jbcred",
    "kardbank",
    "lev consorcio",
    "master",
    "mercantil",
    "meucashcard",
    "novo saque",
    "nyc",
    "ole - orienta",
    "pan",
    "paraná bank",
    "ph",
    "presença bank",
    "quero + crédito",
    "sabemi",
    "safra",
    "santander fve",
    "total cash",
    "v8",
    "vctex",
    "vemcard",
    "via certa",
    "web cash"
  ];

>>>>>>> 182e6f2780f242486f567f7896a25897510b61db

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
                <option value="">Escolha um banco</option>
                {bancos.map((banco) => (
                  <option className='bg-black' value={banco}>{banco}</option>
                ))}
              </select>
              <button className='border rounded-xl p-5 shadow-xl shadow-gray-700 transition-all durarion-400 cursor-pointer hover:bg-gray-300 hover:text-black' type='submit'>{loading ? "Carregando..." : "Criar arquivo"}</button>
            </form>
          </div>
          <img className='w-120 rounded-r-4xl' src={logo} alt="" />
        </div>
      </section>

    </>
  )
}

export default App
