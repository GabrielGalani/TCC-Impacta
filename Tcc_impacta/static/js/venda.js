document.addEventListener('DOMContentLoaded', function() {
    async function fetchPreco(produtoId) {
        try {
            const response = await fetch(`/api/get-produto-preco/${produtoId}/`);
            const data = await response.json();
            return data.preco || 0;
        } catch (error) {
            console.error('Erro ao buscar o preço:', error);
            return 0;
        }
    }

    function atualizarValorTotal(inputQuantidade, inputValorUnitario, inputValorTotal) {
        const quantidade = parseFloat(inputQuantidade.value) || 0;
        const valorUnitario = parseFloat(inputValorUnitario.value) || 0;
        const valorTotal = quantidade * valorUnitario;
        inputValorTotal.value = valorTotal.toFixed(2);

        atualizarValorTotalVenda(); // Atualizar o valor total da venda sempre que o valor total do item for alterado
    }

    function atualizarValorTotalVenda() {
        const valorTotalVenda = Array.from(document.querySelectorAll('.valor-total'))
            .reduce((total, input) => {
                const valor = parseFloat(input.value) || 0;
                console.log(`Valor total do item: ${valor}`); // Adiciona log
                return total + valor;
            }, 0);
        
        console.log(`Valor total da venda: ${valorTotalVenda}`); // Adiciona log
        document.getElementById('valor-total-venda').value = valorTotalVenda.toFixed(2);
    }

    function adicionarEventosSelects(select) {
        select.addEventListener('change', async (event) => {
            const produtoId = event.target.value;
            const inputValorUnitario = event.target.closest('tr').querySelector('.valor-unitario');
            const inputValorTotal = event.target.closest('tr').querySelector('.valor-total');

            if (produtoId) {
                const preco = await fetchPreco(produtoId);
                inputValorUnitario.value = preco;
                atualizarValorTotal(
                    event.target.closest('tr').querySelector('.quantidade'),
                    inputValorUnitario,
                    inputValorTotal
                );
            } else {
                inputValorUnitario.value = '';
                inputValorTotal.value = '';
                atualizarValorTotalVenda();
            }
        });
    }

    function adicionarEventosQuantidades(input) {
        input.addEventListener('input', (event) => {
            const tr = event.target.closest('tr');
            const inputValorUnitario = tr.querySelector('.valor-unitario');
            const inputValorTotal = tr.querySelector('.valor-total');
            atualizarValorTotal(event.target, inputValorUnitario, inputValorTotal);
        });
    }

    function adicionarNovaLinha() {
        const tabelaBody = document.getElementById('item-venda-tbody');
        const novaLinha = tabelaBody.rows[tabelaBody.rows.length - 1].cloneNode(true);

        const inputs = novaLinha.querySelectorAll('input');
        inputs.forEach(input => {
            input.value = ''; // Limpar os valores dos inputs
        });

        const selects = novaLinha.querySelectorAll('select');
        selects.forEach(select => {
            select.value = ''; // Resetar selects
        });

        const novoSelectProduto = novaLinha.querySelector('.produto');
        const novaQuantidade = novaLinha.querySelector('.quantidade');
        adicionarEventosSelects(novoSelectProduto);
        adicionarEventosQuantidades(novaQuantidade);
        adicionarEventosRemover(novaLinha);

        tabelaBody.appendChild(novaLinha);
    }

    document.getElementById('add-item').addEventListener('click', function() {
        adicionarNovaLinha();
    });

    function adicionarEventosRemover(linha) {
        const botaoRemover = linha.querySelector('.remove-item');
        botaoRemover.addEventListener('click', function() {
            linha.remove();
            atualizarValorTotalVenda(); // Atualiza o valor total da venda ao remover uma linha
        });
    }

    // Adiciona eventos aos selects e inputs já existentes
    const selectProdutos = document.querySelectorAll('.produto');
    selectProdutos.forEach(select => {
        adicionarEventosSelects(select);
    });

    const inputQuantidades = document.querySelectorAll('.quantidade');
    inputQuantidades.forEach(input => {
        adicionarEventosQuantidades(input);
    });

    const linhas = document.querySelectorAll('#item-venda-tbody tr');
    linhas.forEach(linha => {
        adicionarEventosRemover(linha);
    });
});
