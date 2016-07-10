 CREATE DATABASE bd_contas
 	WITH ENCODING='UTF-8'
 	OWNER=paulo
 	LC_COLLATE='pt_BR.utf8'
 	LC_CTYPE='pt_BR.utf8';

 DROP DOMAIN lanc_padrao;
 CREATE DOMAIN lanc_padrao AS CHAR(1)
 CHECK(VALUE = 'c' OR VALUE = 'd')
 DEFAULT 'c'
 NOT NULL;


-- DROP TABLE Contas;
 CREATE TABLE contas(
 	id SERIAL PRIMARY KEY,
 	descricao VARCHAR(100) NOT NULL,
 	data_inclusao TIMESTAMP NOT NULL DEFAULT now(),
 	conta_pai INT);
-- 
 ALTER TABLE contas ADD COLUMN lancamento_padrao lanc_padrao;
-- 
 CREATE TABLE pessoas(
 	cpf CHAR(14) PRIMARY KEY,
 	rg CHAR(12),
 	nome VARCHAR(100),
 	data_inclusao TIMESTAMP NOT NULL DEFAULT now());
-- 
 CREATE TABLE lancamentos(
 	id SERIAL PRIMARY KEY,
 	id_conta INT NOT NULL,
 	cpf CHAR(14) NOT NULL,
 	data_vencimento DATE,
 	data_pagamento DATE DEFAULT now(),
 	numero VARCHAR(25),
 	descricao VARCHAR(100) NOT NULL,
 	transferencia INT NOT NULL,
 	lancamento DECIMAL(9, 2),
 	data_inclusao TIMESTAMP NOT NULL DEFAULT now());
-- /* alter table lancamentos drop column id_origem */
 ALTER TABLE lancamentos
 ADD COLUMN id_origem INT NULL;
-- /* ALTER TABLE lancamentos DROP constraint "fk_id_origem" */
 ALTER TABLE lancamentos
 ADD CONSTRAINT "fk_id_origem" FOREIGN KEY(id_origem)
 REFERENCES lancamentos(id)
 ON UPDATE CASCADE ON DELETE CASCADE;
-- 
 ALTER TABLE lancamentos
 ADD CONSTRAINT "fk_cpf" FOREIGN KEY(cpf)
 REFERENCES pessoas(cpf)
 ON UPDATE CASCADE ON DELETE RESTRICT;
-- 
 ALTER TABLE lancamentos
 ADD CONSTRAINT "fk_id_transferencia" FOREIGN KEY(transferencia)
 REFERENCES contas(id)
 ON UPDATE CASCADE ON DELETE RESTRICT;
-- 
 ALTER TABLE lancamentos
 ADD CONSTRAINT "fk_id_conta" FOREIGN KEY(id_conta)
 REFERENCES contas(id)
 ON UPDATE CASCADE ON DELETE RESTRICT;
-- 
 ALTER TABLE contas
 ADD CONSTRAINT "fk_conta_pai" FOREIGN KEY(conta_pai)
 REFERENCES contas(id)
 ON UPDATE CASCADE ON DELETE RESTRICT;
--

-- DROP VIEW vw_lancamento_contas;
--  
 CREATE VIEW vw_lancamento_contas AS
 SELECT
 	lancamentos.id,
 	lancamentos.id_conta,
 	contas.descricao as descricao_conta,
 	lancamentos.cpf,
 	pessoas.nome,
 	lancamentos.data_vencimento,
 	lancamentos.data_pagamento,
 	lancamentos.numero,
 	lancamentos.descricao,
 	lancamentos.transferencia,
 	(SELECT contas.descricao FROM contas WHERE contas.id = lancamentos.transferencia) AS descricao_transferencia,
 	CASE WHEN lancamentos.lancamento < 0 THEN abs(lancamentos.lancamento) ELSE 0
 	END AS debito,
 	CASE WHEN lancamentos.lancamento >= 0 THEN lancamentos.lancamento ELSE 0
 	END AS credito,
 	lancamentos.data_inclusao
 FROM
 	lancamentos
 	INNER JOIN pessoas
 	ON lancamentos.cpf = pessoas.cpf
 	INNER JOIN contas
 	ON contas.id = lancamentos.id_conta;

-- SELECT * FROM vw_lancamento_contas;
-- SELECT * FROM lancamentos;
-- --
 CREATE OR REPLACE FUNCTION inserir_lancamento(
 	id_conta INT,
 	cpf CHAR(14),
 	data_vencimento DATE,
 	data_pagamento DATE,
 	numero VARCHAR(25),
 	descricao VARCHAR(100),
 	transferencia INT,
 	lancamento NUMERIC(9,2),
 	padrao BOOLEAN)
 RETURNS void AS $$
 DECLARE
 	tipo CHAR(1);
 	var_id_origem INT;
 BEGIN
 	if padrao = TRUE THEN
 		tipo := (SELECT lancamento_padrao FROM contas WHERE id = id_conta);
 		IF tipo = 'd' THEN
 			lancamento := -lancamento;
 		END IF;
 	END IF;
	
	INSERT INTO lancamentos(
		id_conta,
		cpf,
		data_vencimento,
		data_pagamento,
		numero,
		descricao,
		transferencia,
		lancamento
	) VALUES (
		id_conta,
		cpf,
		data_vencimento,
		data_pagamento,
		numero,
		descricao,
		transferencia,
		lancamento);

	var_id_origem := (SELECT MAX(id) FROM lancamentos);
	INSERT INTO lancamentos(
		id_conta,
		cpf,
		data_vencimento,
		data_pagamento,
		numero,
		descricao,
		transferencia,
		lancamento,
		id_origem
	) VALUES (
		transferencia,
		cpf,
		data_vencimento,
		data_pagamento,
		numero,
		descricao,
		id_conta,
		-lancamento,
		var_id_origem);

	UPDATE lancamentos 
	SET id_origem = (var_id_origem + 1)
	WHERE id = var_id_origem;
END;
$$ LANGUAGE plpgsql;

/* Lançamentos teste */
-- 
-- INSERT INTO contas(
-- 	descricao, lancamento_padrao)
-- VALUES 
-- 	('Receitas', 'd'),
-- 	('Conta Poupança', 'd'),
-- 	('Conta Corrente', 'd'),
-- 	('Despesas', 'c'),
-- 	('Bradesco', 'd'),
-- 	('Caixa Econômica Federal', 'd'), 
-- 	('Carteira', 'd'),
-- 	('Salário', 'c') ;

-- SELECT * FROM contas;

-- UPDATE contas SET
-- 	conta_pai = 2
-- WHERE id in (5, 6);

-- UPDATE contas SET
-- 	conta_pai = 1
-- WHERE
-- 	id = 8;

-- INSERT INTO pessoas(
-- 	cpf, nome)
-- VALUES(
-- 	'364.388.708-62', 'Paulo C. Silva Jr.');

-- SELECT * FROM pessoas;

-- SELECT inserir_lancamento(8, '364.388.708-62', NULL, '04/07/2016', '01', 'teste01', 6, 800, TRUE);
-- SELECT * FROM vw_lancamento_contas ORDER BY data_inclusao;
-- SELECT * FROM lancamentos;	
-- SELECT * FROM vw_lancamento_contas WHERE id_conta = 6 ORDER BY data_inclusao;