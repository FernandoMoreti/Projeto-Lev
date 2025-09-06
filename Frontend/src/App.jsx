import React, { useState } from 'react'
import './App.css'
import logo from "../public/logo.jpg"

function App() {

  const [file, setFile] = useState("")
  const [banco, setBanco] = useState("")

  const bancos = [
  "Banco do Brasil",
  "Caixa Econômica Federal",
  "Itaú Unibanco",
  "Bradesco",
  "Santander Brasil",
  "Banco Safra",
  "BTG Pactual",
  "Banco Inter",
  "Nubank",
  "C6 Bank",
  "Banco Pan",
  "Banco Original",
  "Banco Neon",
  "Banco Modal",
  "Banco Sofisa",
  "Banco Votorantim (BV)",
  "Banco Daycoval",
  "Banco Alfa",
  "Banco BMG",
  "Banco Mercantil do Brasil",
  "Banco Fibra",
  "Banco Banrisul",
  "Banco Banestes",
  "Banco Sicoob",
  "Banco Sicredi",
  "Banco Agibank",
  "Banco Cetelem",
  "Banco Digio",
  "Banco Renner",
  "Banco Industrial do Brasil",
  "Banco Paulista",
  "Banco Pine",
  "Banco Topázio",
  "Banco Master",
  "Banco Semear",
  "Banco Cruzeiro do Sul",
  "Banco ABC Brasil",
  "Banco Rabobank",
  "Banco Toyota",
  "Banco Honda",
  "Banco RCI Brasil",
  "Banco Mercedes-Benz",
  "Banco Volvo",
  "Banco Volkswagen",
  "Banco PSA Finance",
  "HSBC",
  "Citibank",
  "JPMorgan Chase",
  "Bank of America",
  "Deutsche Bank",
  "BNP Paribas"
];

  return (
    <>
      <section className='flex justify-center items-center h-screen bg-gradient-to-tr from-black to-purple-500'>
        <div className='flex bg-black/10 rounded-4xl shadow-2xl shadow-gray-700'>
          <div className='flex flex-col p-10 w-120'>
            <h1 className='flex justify-center text-xl font-semibold'>Bem vindo ao Conversor WORKBANK</h1>
            <form className='flex flex-col gap-5' action="">
              <p className='text-lg pt-5'>Importe o relatorio:</p>
              <input className="border rounded-xl p-5 shadow-xl shadow-gray-700 cursor-pointer" onChange={(e) => setFile(e.target.files[0])} type="file" />
              <p className='text-lg'>Escolha o banco:</p>
              <select className='border rounded-xl p-5 shadow-xl shadow-gray-700 cursor-pointer' name="Banco" id="">
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
