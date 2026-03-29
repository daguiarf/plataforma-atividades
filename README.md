# 📚 Plataforma de Atividades Escolares

Aplicação web para gerenciamento de atividades escolares, onde professores criam atividades, alunos enviam respostas e professores realizam correções.

---

## 🚀 Como rodar o projeto

### Pré-requisitos

* Docker
* Docker Compose

---

### ▶️ Subindo a aplicação

```bash
docker-compose up --build
```

Aguarde até ver no terminal:

```
Iniciando servidor...
Starting development server at http://0.0.0.0:8000/
```

---

### 🌐 Acesse a aplicação

* Frontend/ Sistema:
  👉 http://localhost:3000

* Admin Django:
  👉 http://localhost:8000/admin

---

## 🔐 Acesso inicial (já configurado)

O sistema cria automaticamente um superusuário.

### Credenciais:

* **Usuário:** admin
* **Senha:** admin

---

## ⚠️ CONFIGURAÇÃO INICIAL OBRIGATÓRIA

> ⚠️ Sem essa configuração, o sistema não funcionará corretamente na avaliação.

---

## 1️⃣ Criar usuários

Acesse:

👉 http://localhost:8000/admin

Entre com:

* admin / admin

Vá em:

👉 **Users (Usuários)**

Crie:

### ✔️ Professor

* Username: professor
* Senha: (defina uma)
* Tipo/Role: **PROFESSOR**

### ✔️ Aluno

* Username: aluno
* Senha: (defina uma)
* Tipo/Role: **ALUNO**

---

## 2️⃣ Criar Turma e fazer associações

Acesse:

👉 **Turmas**

### Passos:

1. Clique em **"Add Turma"**
2. Crie uma turma (ex: "Turma A")
3. Associe o **ALUNO** à turma
4. Salve

---

### 🔴 PASSO CRÍTICO (muito importante)

Após salvar a turma:

1. Clique novamente na turma criada
2. Associe um **PROFESSOR** a essa turma
3. Salve novamente

---

### ⚠️ Atenção

Se você **não associar o professor à turma**:

* Ele **não conseguirá criar atividades**
* Isso pode parecer erro no sistema, mas é regra de negócio

---

## 3️⃣ Criar atividade (fluxo do professor)

Agora faça login como professor:

👉 (via frontend ou API, conforme implementação)

Ação:

* Criar atividade
* Vincular à turma criada

Campos:

* Título
* Descrição
* Turma
* Data de entrega

---

## 4️⃣ Enviar resposta (fluxo do aluno)

Faça login como aluno:

* Visualize atividades disponíveis
* Envie uma resposta

---

## 5️⃣ Correção (fluxo do professor)

Volte ao professor:

* Acesse respostas da atividade
* Atribua:

  * Nota (0 a 10) ✅ obrigatório
  * Feedback (opcional)

---

## 📌 Regras de negócio implementadas

* Aluno pertence a uma turma
* Aluno não pode acessar atividades de outra turma
* Aluno envia apenas **uma resposta por atividade**
* Aluno pode editar resposta antes da data de entrega
* Professor só corrige atividades que criou
* Professor pode editar nota e feedback
* Nota obrigatória entre **0 e 10**

---

## 🧱 Tecnologias utilizadas

* Backend: Django + Django REST Framework
* Banco de dados: MariaDB
* Containerização: Docker + Docker Compose
* Arquitetura: Separação por domínios (inspirado em DDD)

---

## 🧪 Observações importantes para avaliação

* O sistema já sobe com:

  * Banco configurado
  * Migrations aplicadas
  * Superusuário criado automaticamente

* Não é necessário rodar comandos manuais

* O fluxo depende da configuração inicial no admin

---

## ⚠️ Problemas comuns (e como evitar)

### ❌ Professor não consegue criar atividade

✔️ Verifique:

* Se o professor foi associado à turma

---

### ❌ Aluno não vê atividades

✔️ Verifique:

* Se o aluno está na turma correta
* Se a atividade foi criada para essa turma

---

### ❌ Login não funciona

✔️ Verifique:

* Se o usuário foi criado corretamente
* Se a senha foi definida

---

## ✅ Resumo do fluxo correto

1. Login admin
2. Criar professor
3. Criar aluno
4. Criar turma
5. Associar aluno à turma
6. ⚠️ Associar professor à turma
7. Professor cria atividade
8. Aluno responde
9. Professor corrige

---

## 📬 Considerações finais

O sistema foi desenvolvido com foco em clareza de fluxo, regras de negócio bem definidas e facilidade de execução para avaliação técnica.

---
