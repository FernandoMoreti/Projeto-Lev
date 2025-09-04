# 🧠 Guia para Contribuir com Este Projeto no GitHub

Obrigado por querer contribuir com este projeto! 🎉
Siga os passos abaixo para clonar, criar uma branch, fazer alterações e enviar seu Pull Request corretamente.

# ✅ Pré-requisitos

Tenha o Git instalado (instalar Git)

Tenha uma conta no GitHub

(Opcional) Use um editor como o VS Code

# 1. 🔁 Fork do repositório (se necessário)

Se você não for colaborador direto do projeto, comece criando um fork:

Vá até a página do projeto no GitHub.

Clique no botão Fork (no canto superior direito).

Isso criará uma cópia do projeto no seu próprio GitHub.

# 2. 💻 Clone o projeto para sua máquina

Abra o terminal (ou Git Bash) e execute:

```bash
git clone https://github.com/FernandoMoreti/Projeto-Lev
```

# 3. 🌿 Crie uma nova branch

Sempre crie uma branch separada para suas alterações, com um nome descritivo:

```bash
git checkout -b minha-nova-feature
```

Exemplo:

```bash
git checkout -b correcao-botao-login
```

# 4. ✍️ Faça suas alterações

Agora, edite os arquivos no seu editor (VS Code, por exemplo).
Quando terminar:

Adicione as alterações:

```bash
git add .
```

Faça o commit:

```bash
git commit -m "Descrição clara do que foi feito"
```

Exemplo:

```bash
git commit -m "Corrigido bug no botão de login que não redirecionava"
```

# 5. 🚀 Envie sua branch para o GitHub

```bash
git push origin minha-nova-feature
```

# 6. 🔄 Crie um Pull Request

Vá até o repositório no GitHub.

Você verá um botão para criar um Pull Request da sua branch recém-enviada.

Clique em "Compare & Pull Request".

Escreva um título e uma descrição do que foi feito.

Clique em "Create Pull Request".

# 7. ⬇️ Atualize seu repositório local (git pull)

Se quiser atualizar seu repositório com a versão mais recente da branch principal (geralmente main ou master):

```bash
git checkout main
git pull origin main
```

Se quiser atualizar sua branch atual com a última versão da main:

```bash
git checkout minha-nova-feature
git pull origin main
```

❓ Dúvidas?

Se tiver dúvidas ou problemas, sinta-se à vontade para abrir uma Issue
 no repositório.
