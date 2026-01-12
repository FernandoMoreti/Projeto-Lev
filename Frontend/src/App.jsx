import React, { useState, useRef, useEffect } from 'react'
import './App.css'
import logo from "../public/logo.jpg"
import { createScope, createDraggable, createSpring } from "animejs"

function App() {

  const [file, setFile] = useState("")
  const [banco, setBanco] = useState("")
  const [loading, setLoading] = useState(false)
  const [validar, setValidar] = useState(false)
  const [mostrar, setMostrar] = useState(false)
  const [mensagem, setMensagem] = useState(false)

  const root = useRef(null);
  const scope = useRef(null);

  useEffect(() => {
  
    scope.current = createScope({ root }).add( self => {

      createDraggable('.logo', {
        container: [0, 0, 0, 0],
        releaseEase: createSpring({ stiffness: 200 })
      });

    });
    
    // Properly cleanup all anime.js instances declared inside the scope
    return () => scope.current.revert()
    
  }, []);
  
  async function handleSubmit(e) {
    e.preventDefault()

    setLoading(true)

    const formData = new FormData();
    formData.append("banco", banco)
    formData.append("arquivo", file)

    if (file == "" || banco == "") {
      setMensagem(true)
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/executar", {
        method: "POST",
        body: formData,
      })

      if (response.ok){
        const disposition = response.headers.get("content-disposition");
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(disposition);
        let filename = "arquivo.xlsx";

        console.log(disposition)
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '');
          filename = decodeURIComponent(filename);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setValidar(true)
      } else {
        setValidar(false)
      }
    } catch(error) {
      console.log("Erro ao enviar:", error)
      setValidar(false)
    } finally {
      setMostrar(true)
      setLoading(false)

      setTimeout(() => {
        setMensagem(false)
        setMostrar(false)
      }, 2000)
    }
  }

  const bancos = [
    "Aki",
    "Amigoz",
    "Ayude",
    "BRB360",
    "BRBInconta",
    "BTW",
    "Bv",
    "Digio",
    "Euro",
    "Grandino",
    "Happy",
    "Icred",
    "Kardbank",
    "NEO",
    "NYC",
    "PHtech",
    "Presenca",
    "QualiBank",
    "SantanderFVEVI",
    "V8",
    "VCtex",
    "WebCash"
   ]

  return (
    <>
      <div ref={root}>
        <section className='flex flex-col h-screen'>
          <p className={`absolute p-5 w-full text-white transition-opacity duration-500 rounded-b-2xl ${mostrar ? ' opacity-100 ' : ' opacity-0 '}${validar ? 'bg-green-600' : 'bg-red-600'}`}>{validar ? "Editado com sucesso" : mensagem ? "Faltando credenciais" : "Não foi possivel editar"}</p>
          <div className='flex-1 flex justify-center items-center bg-black/10'>
            <div className='flex flex-col p-10 h-120 w-120 shadow-2xl bg-white shadow-gray-700 rounded-l-4xl'>
              <h1 className='flex justify-center text-[22px] font-bold'>Bem vindo ao Conversor WORKBANK</h1>
              <form onSubmit={handleSubmit} className='flex flex-col justify-center h-full' action="">
                <p className='text-lg pt-5 font-semibold'>Importe o relatorio:</p>
                <input className="border mt-2 rounded-xl p-5 shadow-md shadow-gray-700 cursor-pointer" onChange={(e) => setFile(e.target.files[0])} type="file" />
                <p className='text-lg mt-5 font-semibold'>Escolha o banco:</p>
                <select onChange={(e) => {setBanco(e.target.value)}} className='border mt-2 rounded-xl p-5 shadow-md shadow-gray-700 cursor-pointer' name="Banco" id="">
                  <option className='hidden'>Escolha um banco</option>
                  {bancos.map((banco) => (
                    <option value={banco}>{banco}</option>
                  ))}
                </select>
                <button className='mt-5 bg-black text-white rounded-xl p-5 transition-all duration-300 cursor-pointer hover:bg-gray-600 hover:-translate-y-1' type='submit'>{loading ? "Carregando..." : "Criar arquivo"}</button>
              </form>
            </div>
            <img className='logo w-120 rounded-r-4xl shadow-2xl shadow-gray-700' src={logo} alt="" />
          </div>
        </section>
      </div>
    </>
  )
}

export default App
