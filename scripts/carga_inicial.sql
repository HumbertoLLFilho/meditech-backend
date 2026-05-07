-- =============================================================
-- MediTech — Carga Inicial
-- =============================================================
-- • 10 especialidades
-- • 1 admin + 50 médicos ativos + 10 médicos inativos
-- • 10 pacientes (com endereço e dados clínicos de exemplo)
-- • Associações médico ↔ especialidade (todos os 60 médicos)
-- • Horários disponíveis (apenas os 50 ativos, 8 padrões rotacionados)
--
-- Novos campos em usuarios:
--   endereço : cep, logradouro, numero, complemento, bairro, cidade, estado
--   saúde    : tipo_sanguineo, alergias, plano_saude
--
-- Senha padrão: Meditech@2026
-- Requer pgcrypto (disponível nas imagens oficiais do PostgreSQL).
--
-- Execução:
--   psql -U <usuario> -d <banco> -f scripts/carga_inicial.sql
-- =============================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
DECLARE
    v_senha TEXT := crypt('Meditech@2026', gen_salt('bf', 12));
BEGIN

    -- ----------------------------------------------------------
    -- Especialidades
    -- ----------------------------------------------------------
    INSERT INTO especialidades (nome) VALUES
        ('Cardiologia'), ('Dermatologia'), ('Ortopedia'),  ('Pediatria'),
        ('Neurologia'),  ('Oftalmologia'), ('Ginecologia'), ('Urologia'),
        ('Clínica Geral'), ('Psiquiatria')
    ON CONFLICT (nome) DO NOTHING;

    -- ----------------------------------------------------------
    -- Admin
    -- ----------------------------------------------------------
    INSERT INTO usuarios (nome, sobrenome, data_nascimento, genero, email, senha, cpf, telefone, tipo, ativo, data_cadastro)
    VALUES ('Admin','MediTech','1990-01-01','masculino','admin@meditech.com',v_senha,'00000000001','11900000001','admin',true,NOW())
    ON CONFLICT (email) DO NOTHING;

    -- ----------------------------------------------------------
    -- 50 Médicos ativos
    -- ----------------------------------------------------------
    INSERT INTO usuarios (nome, sobrenome, data_nascimento, genero, email, senha, cpf, telefone, tipo, ativo, status_aprovacao, data_cadastro)
    VALUES
        -- Clínica Geral (10)
        ('Ana',      'Lima',      '1985-03-15', 'feminino',  'ana.lima@meditech.com',            v_senha, '00000000002', '11911110002', 'medico', true, 'aprovado', NOW()),
        ('Joao',     'Pereira',   '1980-08-14', 'masculino', 'joao.pereira@meditech.com',        v_senha, '00000000003', '11911110003', 'medico', true, 'aprovado', NOW()),
        ('Carlos',   'Mendes',    '1975-05-20', 'masculino', 'carlos.mendes@meditech.com',       v_senha, '00000000004', '11911110004', 'medico', true, 'aprovado', NOW()),
        ('Fernanda', 'Costa',     '1988-11-30', 'feminino',  'fernanda.costa@meditech.com',      v_senha, '00000000005', '11911110005', 'medico', true, 'aprovado', NOW()),
        ('Roberto',  'Alves',     '1972-04-18', 'masculino', 'roberto.alves@meditech.com',       v_senha, '00000000006', '11911110006', 'medico', true, 'aprovado', NOW()),
        ('Patricia', 'Silva',     '1990-07-25', 'feminino',  'patricia.silva@meditech.com',      v_senha, '00000000007', '11911110007', 'medico', true, 'aprovado', NOW()),
        ('Marcos',   'Santos',    '1983-09-12', 'masculino', 'marcos.santos@meditech.com',       v_senha, '00000000008', '11911110008', 'medico', true, 'aprovado', NOW()),
        ('Luciana',  'Ferreira',  '1978-02-28', 'feminino',  'luciana.ferreira@meditech.com',    v_senha, '00000000009', '11911110009', 'medico', true, 'aprovado', NOW()),
        ('Eduardo',  'Rocha',     '1986-06-15', 'masculino', 'eduardo.rocha@meditech.com',       v_senha, '00000000010', '11911110010', 'medico', true, 'aprovado', NOW()),
        ('Camila',   'Oliveira',  '1992-12-03', 'feminino',  'camila.oliveira@meditech.com',     v_senha, '00000000011', '11911110011', 'medico', true, 'aprovado', NOW()),
        -- Cardiologia (5)
        ('Henrique', 'Souza',     '1970-12-03', 'masculino', 'henrique.souza@meditech.com',      v_senha, '00000000012', '11911110012', 'medico', true, 'aprovado', NOW()),
        ('Marina',   'Barbosa',   '1983-07-17', 'feminino',  'marina.barbosa@meditech.com',      v_senha, '00000000013', '11911110013', 'medico', true, 'aprovado', NOW()),
        ('Felipe',   'Castro',    '1977-03-22', 'masculino', 'felipe.castro@meditech.com',       v_senha, '00000000014', '11911110014', 'medico', true, 'aprovado', NOW()),
        ('Renata',   'Lima',      '1985-01-14', 'feminino',  'renata.lima@meditech.com',         v_senha, '00000000015', '11911110015', 'medico', true, 'aprovado', NOW()),
        ('Thiago',   'Nunes',     '1979-08-30', 'masculino', 'thiago.nunes@meditech.com',        v_senha, '00000000016', '11911110016', 'medico', true, 'aprovado', NOW()),
        -- Dermatologia (5)
        ('Carla',    'Ferreira',  '1990-11-08', 'feminino',  'carla.ferreira@meditech.com',      v_senha, '00000000017', '11911110017', 'medico', true, 'aprovado', NOW()),
        ('Gabriel',  'Ribeiro',   '1987-04-25', 'masculino', 'gabriel.ribeiro@meditech.com',     v_senha, '00000000018', '11911110018', 'medico', true, 'aprovado', NOW()),
        ('Isabela',  'Martins',   '1987-04-07', 'feminino',  'isabela.martins@meditech.com',     v_senha, '00000000019', '11911110019', 'medico', true, 'aprovado', NOW()),
        ('Rafael',   'Teixeira',  '1984-09-16', 'masculino', 'rafael.teixeira@meditech.com',     v_senha, '00000000020', '11911110020', 'medico', true, 'aprovado', NOW()),
        ('Juliana',  'Gomes',     '1993-02-19', 'feminino',  'juliana.gomes@meditech.com',       v_senha, '00000000021', '11911110021', 'medico', true, 'aprovado', NOW()),
        -- Ortopedia (5)
        ('Bruno',    'Santos',    '1978-07-22', 'masculino', 'bruno.santos@meditech.com',        v_senha, '00000000022', '11911110022', 'medico', true, 'aprovado', NOW()),
        ('Fernando', 'Rocha',     '1988-01-25', 'masculino', 'fernando.rocha@meditech.com',      v_senha, '00000000023', '11911110023', 'medico', true, 'aprovado', NOW()),
        ('Leticia',  'Cardoso',   '1991-05-11', 'feminino',  'leticia.cardoso@meditech.com',     v_senha, '00000000024', '11911110024', 'medico', true, 'aprovado', NOW()),
        ('Andre',    'Monteiro',  '1976-10-08', 'masculino', 'andre.monteiro@meditech.com',      v_senha, '00000000025', '11911110025', 'medico', true, 'aprovado', NOW()),
        ('Tatiane',  'Correia',   '1989-03-27', 'feminino',  'tatiane.correia@meditech.com',     v_senha, '00000000026', '11911110026', 'medico', true, 'aprovado', NOW()),
        -- Pediatria (5)
        ('Elena',    'Costa',     '1975-09-12', 'feminino',  'elena.costa@meditech.com',         v_senha, '00000000027', '11911110027', 'medico', true, 'aprovado', NOW()),
        ('Viviane',  'Pereira',   '1986-06-20', 'feminino',  'viviane.pereira@meditech.com',     v_senha, '00000000028', '11911110028', 'medico', true, 'aprovado', NOW()),
        ('Leonardo', 'Freitas',   '1981-11-15', 'masculino', 'leonardo.freitas@meditech.com',    v_senha, '00000000029', '11911110029', 'medico', true, 'aprovado', NOW()),
        ('Sandra',   'Moreira',   '1974-08-07', 'feminino',  'sandra.moreira@meditech.com',      v_senha, '00000000030', '11911110030', 'medico', true, 'aprovado', NOW()),
        ('Rodrigo',  'Pinto',     '1992-04-03', 'masculino', 'rodrigo.pinto@meditech.com',       v_senha, '00000000031', '11911110031', 'medico', true, 'aprovado', NOW()),
        -- Neurologia (5)
        ('Diego',    'Oliveira',  '1982-05-30', 'masculino', 'diego.oliveira@meditech.com',      v_senha, '00000000032', '11911110032', 'medico', true, 'aprovado', NOW()),
        ('Aline',    'Sousa',     '1988-09-21', 'feminino',  'aline.sousa@meditech.com',         v_senha, '00000000033', '11911110033', 'medico', true, 'aprovado', NOW()),
        ('Marcelo',  'Cunha',     '1975-02-14', 'masculino', 'marcelo.cunha@meditech.com',       v_senha, '00000000034', '11911110034', 'medico', true, 'aprovado', NOW()),
        ('Priscila', 'Lopes',     '1991-07-08', 'feminino',  'priscila.lopes@meditech.com',      v_senha, '00000000035', '11911110035', 'medico', true, 'aprovado', NOW()),
        ('Gustavo',  'Ramos',     '1979-12-25', 'masculino', 'gustavo.ramos@meditech.com',       v_senha, '00000000036', '11911110036', 'medico', true, 'aprovado', NOW()),
        -- Oftalmologia (5)
        ('Beatriz',  'Araujo',    '1986-03-18', 'feminino',  'beatriz.araujo@meditech.com',      v_senha, '00000000037', '11911110037', 'medico', true, 'aprovado', NOW()),
        ('Cesar',    'Nogueira',  '1980-11-05', 'masculino', 'cesar.nogueira@meditech.com',      v_senha, '00000000038', '11911110038', 'medico', true, 'aprovado', NOW()),
        ('Daniela',  'Fonseca',   '1993-06-29', 'feminino',  'daniela.fonseca@meditech.com',     v_senha, '00000000039', '11911110039', 'medico', true, 'aprovado', NOW()),
        ('Emerson',  'Viana',     '1977-09-13', 'masculino', 'emerson.viana@meditech.com',       v_senha, '00000000040', '11911110040', 'medico', true, 'aprovado', NOW()),
        ('Fabiana',  'Azevedo',   '1984-01-22', 'feminino',  'fabiana.azevedo@meditech.com',     v_senha, '00000000041', '11911110041', 'medico', true, 'aprovado', NOW()),
        -- Ginecologia (5)
        ('Gabriela', 'Alves',     '1993-06-18', 'feminino',  'gabriela.alves@meditech.com',      v_senha, '00000000042', '11911110042', 'medico', true, 'aprovado', NOW()),
        ('Helena',   'Braga',     '1978-04-15', 'feminino',  'helena.braga@meditech.com',        v_senha, '00000000043', '11911110043', 'medico', true, 'aprovado', NOW()),
        ('Igor',     'Campos',    '1985-08-30', 'masculino', 'igor.campos@meditech.com',         v_senha, '00000000044', '11911110044', 'medico', true, 'aprovado', NOW()),
        ('Joana',    'Dias',      '1990-02-11', 'feminino',  'joana.dias@meditech.com',          v_senha, '00000000045', '11911110045', 'medico', true, 'aprovado', NOW()),
        ('Keila',    'Esteves',   '1987-10-05', 'feminino',  'keila.esteves@meditech.com',       v_senha, '00000000046', '11911110046', 'medico', true, 'aprovado', NOW()),
        -- Urologia (5)
        ('Leandro',  'Faria',     '1973-07-19', 'masculino', 'leandro.faria@meditech.com',       v_senha, '00000000047', '11911110047', 'medico', true, 'aprovado', NOW()),
        ('Milena',   'Galvao',    '1989-11-28', 'feminino',  'milena.galvao@meditech.com',       v_senha, '00000000048', '11911110048', 'medico', true, 'aprovado', NOW()),
        ('Nathan',   'Henriques', '1982-05-14', 'masculino', 'nathan.henriques@meditech.com',    v_senha, '00000000049', '11911110049', 'medico', true, 'aprovado', NOW()),
        ('Olivia',   'Ribeiro',   '1989-11-14', 'feminino',  'olivia.ribeiro@meditech.com',      v_senha, '00000000050', '11911110050', 'medico', true, 'aprovado', NOW()),
        ('Pedro',    'Jardim',    '1976-03-07', 'masculino', 'pedro.jardim@meditech.com',        v_senha, '00000000051', '11911110051', 'medico', true, 'aprovado', NOW())
    ON CONFLICT (email) DO NOTHING;

    -- ----------------------------------------------------------
    -- 10 Médicos inativos
    -- ----------------------------------------------------------
    INSERT INTO usuarios (nome, sobrenome, data_nascimento, genero, email, senha, cpf, telefone, tipo, ativo, status_aprovacao, data_cadastro)
    VALUES
        ('Karine',  'Silva',    '1995-02-20', 'feminino',  'karine.silva@meditech.com',      v_senha, '00000000052', '11922220052', 'medico', false, 'novo', NOW()),
        ('Lucas',   'Nunes',    '1992-10-05', 'masculino', 'lucas.nunes@meditech.com',       v_senha, '00000000053', '11922220053', 'medico', false, 'novo', NOW()),
        ('Nelson',  'Barbosa',  '1976-03-28', 'masculino', 'nelson.barbosa@meditech.com',    v_senha, '00000000054', '11922220054', 'medico', false, 'novo', NOW()),
        ('Paulo',   'Mendes',   '1984-06-09', 'masculino', 'paulo.mendes@meditech.com',      v_senha, '00000000055', '11922220055', 'medico', false, 'novo', NOW()),
        ('Rafaela', 'Teixeira', '1991-09-23', 'feminino',  'rafaela.teixeira@meditech.com',  v_senha, '00000000056', '11922220056', 'medico', false, 'novo', NOW()),
        ('Silvia',  'Matos',    '1988-12-17', 'feminino',  'silvia.matos@meditech.com',      v_senha, '00000000057', '11922220057', 'medico', false, 'novo', NOW()),
        ('Tiago',   'Carvalho', '1981-04-26', 'masculino', 'tiago.carvalho@meditech.com',    v_senha, '00000000058', '11922220058', 'medico', false, 'novo', NOW()),
        ('Ursula',  'Peixoto',  '1994-07-10', 'feminino',  'ursula.peixoto@meditech.com',    v_senha, '00000000059', '11922220059', 'medico', false, 'novo', NOW()),
        ('Victor',  'Queiroz',  '1979-01-15', 'masculino', 'victor.queiroz@meditech.com',    v_senha, '00000000060', '11922220060', 'medico', false, 'novo', NOW()),
        ('Wanda',   'Rezende',  '1986-05-22', 'feminino',  'wanda.rezende@meditech.com',     v_senha, '00000000061', '11922220061', 'medico', false, 'novo', NOW())
    ON CONFLICT (email) DO NOTHING;

    -- ----------------------------------------------------------
    -- Associações médico ↔ especialidade
    -- ----------------------------------------------------------
    -- Clínica Geral (10 ativos + 1 inativo)
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('ana.lima@meditech.com','joao.pereira@meditech.com','carlos.mendes@meditech.com',
                      'fernanda.costa@meditech.com','roberto.alves@meditech.com','patricia.silva@meditech.com',
                      'marcos.santos@meditech.com','luciana.ferreira@meditech.com','eduardo.rocha@meditech.com',
                      'camila.oliveira@meditech.com','rafaela.teixeira@meditech.com')
      AND e.nome = 'Clínica Geral'
    ON CONFLICT DO NOTHING;

    -- Cardiologia
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('henrique.souza@meditech.com','marina.barbosa@meditech.com','felipe.castro@meditech.com',
                      'renata.lima@meditech.com','thiago.nunes@meditech.com','tiago.carvalho@meditech.com')
      AND e.nome = 'Cardiologia'
    ON CONFLICT DO NOTHING;

    -- Dermatologia
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('carla.ferreira@meditech.com','gabriel.ribeiro@meditech.com','isabela.martins@meditech.com',
                      'rafael.teixeira@meditech.com','juliana.gomes@meditech.com','silvia.matos@meditech.com')
      AND e.nome = 'Dermatologia'
    ON CONFLICT DO NOTHING;

    -- Ortopedia
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('bruno.santos@meditech.com','fernando.rocha@meditech.com','leticia.cardoso@meditech.com',
                      'andre.monteiro@meditech.com','tatiane.correia@meditech.com','nelson.barbosa@meditech.com')
      AND e.nome = 'Ortopedia'
    ON CONFLICT DO NOTHING;

    -- Pediatria
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('elena.costa@meditech.com','viviane.pereira@meditech.com','leonardo.freitas@meditech.com',
                      'sandra.moreira@meditech.com','rodrigo.pinto@meditech.com','ursula.peixoto@meditech.com')
      AND e.nome = 'Pediatria'
    ON CONFLICT DO NOTHING;

    -- Neurologia
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('diego.oliveira@meditech.com','aline.sousa@meditech.com','marcelo.cunha@meditech.com',
                      'priscila.lopes@meditech.com','gustavo.ramos@meditech.com','paulo.mendes@meditech.com')
      AND e.nome = 'Neurologia'
    ON CONFLICT DO NOTHING;

    -- Oftalmologia
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('beatriz.araujo@meditech.com','cesar.nogueira@meditech.com','daniela.fonseca@meditech.com',
                      'emerson.viana@meditech.com','fabiana.azevedo@meditech.com','victor.queiroz@meditech.com')
      AND e.nome = 'Oftalmologia'
    ON CONFLICT DO NOTHING;

    -- Ginecologia
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('gabriela.alves@meditech.com','helena.braga@meditech.com','igor.campos@meditech.com',
                      'joana.dias@meditech.com','keila.esteves@meditech.com','wanda.rezende@meditech.com')
      AND e.nome = 'Ginecologia'
    ON CONFLICT DO NOTHING;

    -- Urologia
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('leandro.faria@meditech.com','milena.galvao@meditech.com','nathan.henriques@meditech.com',
                      'olivia.ribeiro@meditech.com','pedro.jardim@meditech.com')
      AND e.nome = 'Urologia'
    ON CONFLICT DO NOTHING;

    -- Psiquiatria (inativos)
    INSERT INTO medico_especialidades (medico_id, especialidade_id)
    SELECT u.id, e.id FROM usuarios u, especialidades e
    WHERE u.email IN ('karine.silva@meditech.com','lucas.nunes@meditech.com')
      AND e.nome = 'Psiquiatria'
    ON CONFLICT DO NOTHING;

    -- ----------------------------------------------------------
    -- Horários disponíveis — 50 médicos ativos, 8 padrões rotacionados
    -- dia_semana: 0=seg 1=ter 2=qua 3=qui 4=sex 5=sab
    -- especialidade_id obtido via JOIN com medico_especialidades (1 espec por médico ativo)
    -- ----------------------------------------------------------

    -- Padrão 0 — seg/qua/sex manhã  (índices 0,8,16,24,32,40,48)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (0,'manha'),(2,'manha'),(4,'manha')) AS d(dia,periodo)
    WHERE u.email IN ('ana.lima@meditech.com','eduardo.rocha@meditech.com','gabriel.ribeiro@meditech.com',
                      'tatiane.correia@meditech.com','marcelo.cunha@meditech.com',
                      'gabriela.alves@meditech.com','olivia.ribeiro@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- Padrão 1 — ter/qui tarde  (índices 1,9,17,25,33,41,49)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (1,'tarde'),(3,'tarde')) AS d(dia,periodo)
    WHERE u.email IN ('joao.pereira@meditech.com','camila.oliveira@meditech.com','isabela.martins@meditech.com',
                      'elena.costa@meditech.com','priscila.lopes@meditech.com',
                      'helena.braga@meditech.com','pedro.jardim@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- Padrão 2 — seg/qua/sex tarde  (índices 2,10,18,26,34,42)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (0,'tarde'),(2,'tarde'),(4,'tarde')) AS d(dia,periodo)
    WHERE u.email IN ('carlos.mendes@meditech.com','henrique.souza@meditech.com','rafael.teixeira@meditech.com',
                      'viviane.pereira@meditech.com','gustavo.ramos@meditech.com','igor.campos@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- Padrão 3 — ter/qui/sab manhã  (índices 3,11,19,27,35,43)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (1,'manha'),(3,'manha'),(5,'manha')) AS d(dia,periodo)
    WHERE u.email IN ('fernanda.costa@meditech.com','marina.barbosa@meditech.com','juliana.gomes@meditech.com',
                      'leonardo.freitas@meditech.com','beatriz.araujo@meditech.com','joana.dias@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- Padrão 4 — seg manhã, ter tarde, qui manhã, sex tarde  (índices 4,12,20,28,36,44)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (0,'manha'),(1,'tarde'),(3,'manha'),(4,'tarde')) AS d(dia,periodo)
    WHERE u.email IN ('roberto.alves@meditech.com','felipe.castro@meditech.com','bruno.santos@meditech.com',
                      'sandra.moreira@meditech.com','cesar.nogueira@meditech.com','keila.esteves@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- Padrão 5 — qua/qui/sex noite  (índices 5,13,21,29,37,45)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (2,'noite'),(3,'noite'),(4,'noite')) AS d(dia,periodo)
    WHERE u.email IN ('patricia.silva@meditech.com','renata.lima@meditech.com','fernando.rocha@meditech.com',
                      'rodrigo.pinto@meditech.com','daniela.fonseca@meditech.com','leandro.faria@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- Padrão 6 — seg manhã, ter noite, qua tarde, sex manhã  (índices 6,14,22,30,38,46)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (0,'manha'),(1,'noite'),(2,'tarde'),(4,'manha')) AS d(dia,periodo)
    WHERE u.email IN ('marcos.santos@meditech.com','thiago.nunes@meditech.com','leticia.cardoso@meditech.com',
                      'diego.oliveira@meditech.com','emerson.viana@meditech.com','milena.galvao@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- Padrão 7 — ter manhã, qui tarde, sab manhã  (índices 7,15,23,31,39,47)
    INSERT INTO horarios_disponiveis (medico_id, especialidade_id, dia_semana, periodo)
    SELECT u.id, me.especialidade_id, d.dia, d.periodo
    FROM usuarios u
    JOIN medico_especialidades me ON me.medico_id = u.id
    CROSS JOIN (VALUES (1,'manha'),(3,'tarde'),(5,'manha')) AS d(dia,periodo)
    WHERE u.email IN ('luciana.ferreira@meditech.com','carla.ferreira@meditech.com','andre.monteiro@meditech.com',
                      'aline.sousa@meditech.com','fabiana.azevedo@meditech.com','nathan.henriques@meditech.com')
    ON CONFLICT ON CONSTRAINT uq_medico_esp_dia_periodo DO NOTHING;

    -- ----------------------------------------------------------
    -- 10 Pacientes (com endereço e dados clínicos de exemplo)
    -- ----------------------------------------------------------
    INSERT INTO usuarios (
        nome, sobrenome, data_nascimento, genero, email, senha, cpf, telefone,
        tipo, ativo,
        cep, logradouro, numero, complemento, bairro, cidade, estado,
        tipo_sanguineo, alergias, plano_saude,
        data_cadastro
    ) VALUES
        ('Alice',    'Mendes',    '1995-04-12', 'feminino',  'alice.mendes@email.com',    v_senha, '20000000001', '11944440001', 'paciente', true,
         '01310100', 'Avenida Paulista',      '1000', 'Apto 42',   'Bela Vista',   'São Paulo',     'SP', 'O+',  NULL,                   'Unimed',          NOW()),
        ('Bruno',    'Carvalho',  '1988-09-03', 'masculino', 'bruno.carvalho@email.com',  v_senha, '20000000002', '11944440002', 'paciente', true,
         '20040020', 'Avenida Rio Branco',    '156', NULL,         'Centro',        'Rio de Janeiro','RJ', 'A-',  'Dipirona',             'Amil',            NOW()),
        ('Clarice',  'Goncalves', '1992-07-20', 'feminino',  'clarice.goncalves@email.com',v_senha,'20000000003', '11944440003', 'paciente', true,
         '30130010', 'Rua dos Caetés',        '320', 'Sala 5',     'Centro',        'Belo Horizonte','MG', 'B+',  NULL,                   NULL,              NOW()),
        ('Daniel',   'Figueiredo','1980-11-28', 'masculino', 'daniel.figueiredo@email.com',v_senha,'20000000004', '11944440004', 'paciente', true,
         '40020010', 'Avenida Sete de Setembro','450',NULL,        'Mercês',        'Salvador',      'BA', 'AB+', 'Penicilina, Ibuprofeno','Bradesco Saúde',  NOW()),
        ('Elena',    'Machado',   '2000-02-14', 'feminino',  'elena.machado@email.com',   v_senha, '20000000005', '11944440005', 'paciente', true,
         '80010020', 'Rua XV de Novembro',    '800', 'Cobertura',  'Centro',        'Curitiba',      'PR', 'O-',  NULL,                   'SulAmérica',      NOW()),
        ('Fabio',    'Nascimento', '1975-06-08','masculino', 'fabio.nascimento@email.com', v_senha, '20000000006', '11944440006', 'paciente', true,
         '51021530', 'Avenida Boa Viagem',    '2200',NULL,         'Boa Viagem',    'Recife',        'PE', 'A+',  'Látex',                'Porto Seguro',    NOW()),
        ('Giovanna', 'Batista',   '1998-12-30', 'feminino',  'giovanna.batista@email.com', v_senha,'20000000007', '11944440007', 'paciente', true,
         '60160080', 'Rua Guilherme Rocha',   '500', 'Apto 301',  'Centro',        'Fortaleza',     'CE', 'B-',  NULL,                   NULL,              NOW()),
        ('Henrique', 'Moura',     '1983-03-17', 'masculino', 'henrique.moura@email.com',  v_senha, '20000000008', '11944440008', 'paciente', true,
         NULL,        NULL,                    NULL,  NULL,         NULL,            NULL,            NULL, 'AB-', 'Sulfa',                'Notredame Intermédica', NOW()),
        ('Isabela',  'Vieira',    '1990-08-22', 'feminino',  'isabela.vieira@email.com',  v_senha, '20000000009', '11944440009', 'paciente', true,
         '69010060', 'Avenida Eduardo Ribeiro','620', NULL,        'Centro',        'Manaus',        'AM', 'O+',  NULL,                   'Hapvida',         NOW()),
        ('Jorge',    'Medeiros',  '1969-05-01', 'masculino', 'jorge.medeiros@email.com',  v_senha, '20000000010', '11944440010', 'paciente', true,
         NULL,        NULL,                    NULL,  NULL,         NULL,            NULL,            NULL, NULL,  NULL,                   NULL,              NOW())
    ON CONFLICT (email) DO NOTHING;

    RAISE NOTICE 'Carga inicial concluída: 10 especialidades | 1 admin | 50 médicos ativos | 10 inativos | 10 pacientes.';
    RAISE NOTICE 'Senha padrão: Meditech@2026';

END $$;
