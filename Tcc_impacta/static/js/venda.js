// Espera o documento ser totalmente carregado antes de executar o código
document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('item-venda-tbody');
    const addButton = document.getElementById('add-item');
    const produtoDataElement = document.getElementById('produto-data');
    let produtoData = [];
    let itemIndex = tbody.querySelectorAll('tr').length;

    // Verifica se o elemento produtoDataElement existe
    if (produtoDataElement) {
        try {
            produtoData = JSON.parse(produtoDataElement.textContent || '[]');
            console.log('Produto Data:', produtoData); // Verifica dados
        } catch (error) {
            console.error('Erro ao parsear JSON:', error);
        }
    }

    // Função para buscar o preço de um produto com base no ID
    function fetchPreco(produtoId, inputElement) {
        fetch(`/api/get-produto-preco/${produtoId}/`)
            .then(response => response.json())
            .then(data => {
                console.log(`Valor Unitário para ID ${produtoId}:`, data.valor_unitario);
                if (data.valor_unitario) {
                    inputElement.value = data.valor_unitario;
                    atualizarValorTotal(inputElement);
                    console.log(`Valor Unitário atualizado para ${inputElement.name}:`, inputElement.value);
                } else {
                    inputElement.value = '0.00';
                }
            })
            .catch(error => {
                console.error('Erro ao buscar o valor do produto:', error);
                inputElement.value = '0.00';
            });
    };

    // Função para atualizar o valor total de um item na tabela
    function atualizarValorTotal(inputElement) {
        const row = inputElement.closest('tr');
        const quantidadeInput = row.querySelector('.quantidade');
        const valorUnitarioInput = row.querySelector('.valor-unitario');
        const valorTotalElement = row.querySelector('.valor-total');
    
        if (quantidadeInput && valorUnitarioInput && valorTotalElement) {
            const quantidade = parseFloat(quantidadeInput.value) || 0;
            const valorUnitario = parseFloat(valorUnitarioInput.value) || 0;
            const valorTotal = quantidade * valorUnitario;
    
            console.log(`Quantidade: ${quantidade}, Valor Unitário: ${valorUnitario}, Valor Total: ${valorTotal}`);
    
            valorTotalElement.textContent = valorTotal.toFixed(2);
        }
    };

    // Função para atualizar o valor unitário quando um produto é selecionado
    function atualizarValorUnitario(selectElement) {
        const produtoId = selectElement.value;
        const valorUnitarioInput = selectElement.closest('tr').querySelector('.valor-unitario');
        fetchPreco(produtoId, valorUnitarioInput);
    };

    // Função para buscar os dados dos produtos
    function fetchProdutos() {
        fetch('/api/get-produtos/')
            .then(response => response.json())
            .then(data => {
                if (data.produtos) {
                    produtoDataElement.textContent = JSON.stringify(data.produtos);
                    console.log('Dados dos produtos atualizados:', data.produtos);
                    produtoData = data.produtos;

                    // Repreencher os selects
                    const selects = document.querySelectorAll('.produto');
                    selects.forEach(select => preencherSelect(select));
                }
            })
            .catch(error => {
                console.error('Erro ao buscar dados dos produtos:', error);
            });
    };

    // Função para preencher um elemento select com as opções de produtos
    function preencherSelect(selectElement) {
        selectElement.innerHTML = ''; // Limpa o conteúdo existente
    
        produtoData.forEach(produto => {
            const option = document.createElement('option');
            option.value = produto.id;
            option.textContent = produto.nome;
            selectElement.appendChild(option);
        });
    
        console.log('Select preenchido com opções:', selectElement); // Verificar se o select é preenchido
    }

    // Função para adicionar uma nova linha de item na tabela de vendas
    function addItem() {
        itemIndex++;
        const newRow = document.createElement('tr');
    
        newRow.innerHTML = `
            <td>
                <select name="form-${itemIndex}-produto" class="produto">
                    <!-- Options will be added here dynamically -->
                </select>
            </td>
            <td>
                <input type="number" name="form-${itemIndex}-quantidade" class="quantidade" min="0" step="1">
            </td>
            <td>
                <input type="text" name="form-${itemIndex}-valor_unitario" class="valor-unitario" readonly>
            </td>
            <td>
                <span class="valor-total">0.00</span>
            </td>
            <td>
                <button type="button" class="remove-item">Remover</button>
            </td>
        `;
    
        tbody.appendChild(newRow);
    
        const newSelect = newRow.querySelector('.produto');
        preencherSelect(newSelect);
    
        // Anexar o evento change ao select depois que ele foi preenchido
        newSelect.addEventListener('change', function () {
            const produtoId = newSelect.value;
            console.log('Produto ID dentro do addItem: ' + produtoId);
            const valorUnitarioInput = newRow.querySelector('.valor-unitario');
            fetchPreco(produtoId, valorUnitarioInput);
        });
    
        const quantidadeInput = newRow.querySelector('.quantidade');
        quantidadeInput.addEventListener('input', function () {
            atualizarValorTotal(quantidadeInput);
        });
    };

    // Busca os dados dos produtos ao carregar a página
    fetchProdutos();

    // Evento para atualizar o valor unitário quando um produto é selecionado
    tbody.addEventListener('change', function (event) {
        if (event.target.name && event.target.name.endsWith('produto')) {
            const produtoId = event.target.value;
            const valorUnitarioInput = event.target.closest('tr').querySelector('.valor-unitario');
            
            if (valorUnitarioInput) {
                fetchPreco(produtoId, valorUnitarioInput);
            }
        }
    });

    // Evento para atualizar o valor total quando a quantidade é alterada
    tbody.addEventListener('input', function (event) {
        if (event.target.classList.contains('quantidade')) {
            atualizarValorTotal(event.target);
        }
    });

    // Evento para remover uma linha da tabela
    tbody.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-item')) {
            event.target.closest('tr').remove();
        }
    });

    // Evento para adicionar um novo item ao clicar no botão de adicionar
    addButton.addEventListener('click', addItem);

    // Eventos para atualizar o valor total nos campos de quantidade existentes
    document.querySelectorAll('.quantidade').forEach(input => {
        input.addEventListener('input', function () {
            atualizarValorTotal(input);
        });
    });
    
    // Eventos para atualizar o valor unitário nos selects de produtos existentes
    document.querySelectorAll('.produto').forEach(select => {
        select.addEventListener('change', function () {
            atualizarValorUnitario(select);
        });
    });

});


// Backup 
    // function atualizarValorTotal(inputElement) {
    //     const row = inputElement.closest('tr');
    //     const quantidadeInput = row.querySelector('.quantidade');
    //     const valorUnitarioInput = row.querySelector('.valor-unitario');
    //     const valorTotalElement = row.querySelector('.valor-total');

    //     if (quantidadeInput && valorUnitarioInput && valorTotalElement) {
    //         const quantidade = parseFloat(quantidadeInput.value) || 0;
    //         const valorUnitario = parseFloat(valorUnitarioInput.value) || 0;
    //         const valorTotal = quantidade * valorUnitario;

    //         console.log(`Quantidade: ${quantidade}, Valor Unitário: ${valorUnitario}, Valor Total: ${valorTotal}`);

    //         valorTotalElement.textContent = valorTotal.toFixed(2);
    //     }
    // };
    

     // function addItem() {
    //     itemIndex++;
    //     const newRow = document.createElement('tr');
        
    //     newRow.innerHTML = `
    //         <td>
    //             <select name="form-${itemIndex}-produto" class="produto">
    //                 <!-- Options will be added here dynamically -->
    //             </select>
    //         </td>
    //         <td>
    //             <input type="number" name="form-${itemIndex}-quantidade" class="quantidade" min="0" step="1">
    //         </td>
    //         <td>
    //             <input type="text" name="form-${itemIndex}-valor_unitario" class="valor-unitario" readonly>
    //         </td>
    //         <td>
    //             <span class="valor-total">0.00</span>
    //         </td>
    //         <td>
    //             <button type="button" class="remove-item">Remover</button>
    //         </td>
    //     `;
        
    //     tbody.appendChild(newRow);
    //     const newSelect = newRow.querySelector('.produto');
    //     preencherSelect(newSelect); // Preencher o select com as opções

    //     // Adicionar o evento de mudança ao novo select
    //     newSelect.addEventListener('change', function () {
    //         atualizarValorUnitario(newSelect);
    //     });
    // };