USE DW
/*
SELECT 
    nota_fiscal_id AS x, 
    valor_total AS y
FROM Venda
WHERE (cliente_id = 1)
AND (usuario_id = <vendedor_id> OR <vendedor_id> IS NULL)
*/ 


select
    *
from 
    cadastro_venda