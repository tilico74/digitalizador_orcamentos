 // Referências do DOM
    const input_uf = document.getElementById('modal_inp_uf');
    const municipioSelect = document.getElementById('modal_inp_municipio');
    const inputEndereco = document.getElementById('modal_inp_endereco');
    const containerResultados = document.getElementById('linhas_endereco');
    const headerResultados = document.getElementById('header_resultado');

    headerResultados.style.display = 'none'; // Esconde o cabeçalho inicialmente

    function carregarMunicipios(uf) {
        municipioSelect.innerHTML = "<option>Carregando...</option>";
        const url_municipios = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios`;

        fetch(url_municipios)
            .then(response => response.json())
            .then(municipios => {
                municipioSelect.innerHTML = "";
                municipios.forEach(municipio => {
                    const option = document.createElement('option');
                    option.value = municipio.nome;
                    option.textContent = municipio.nome;
                    municipioSelect.appendChild(option);
                });
            })
            .catch(err => console.error("Erro ao carregar municípios:", err));
    }

    // Carregamento inicial
    carregarMunicipios(input_uf.value);

    input_uf.addEventListener('change', function () {
        carregarMunicipios(this.value);
    });

    async function buscarEndereco() {
        const uf = input_uf.value;
        const municipio = municipioSelect.value;
        const endereco = inputEndereco.value;

        if (endereco.length < 3) return; // Evita buscas com poucas letras

        const url = `https://viacep.com.br/ws/${uf}/${encodeURIComponent(municipio)}/${encodeURIComponent(endereco)}/json/`;

        try {
            const resposta = await fetch(url);
            const dados = await resposta.json();

            if (Array.isArray(dados)) {
                containerResultados.innerHTML = ""; // Limpa a tabela para novos resultados

                dados.forEach(item => {
                    // Aqui você pode criar as linhas dinamicamente usando as classes que você definiu
                    const div = document.createElement('div');
                    div.className = "grid grid-cols-12 gap-2 rounded-md ring-2 ring-blue-600 bg-blue-50 p-2 sm:ring-0 md:p-0 mb-2 md:mb-0 md:bg-transparent hover:bg-gray-200 cursor-pointer";
                    div.innerHTML = `
                        <div class="col-span-12 sm:col-span-3 relative py-2">
                            <label class="absolute left-3 top-[-1px] text-[12px] text-blue-700 bg-white px-1 leading-none pointer-events-none sm:hidden">Endereço</label>
                            <div class="w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 md:w-auto md:rounded-none md:ring-0 md:px-0 md:py-0 md:text-inherit md:bg-transparent truncate">
                                ${item.logradouro}
                            </div>
                        </div>
                        <div class="col-span-12 sm:col-span-2 relative py-2">
                            <label class="absolute left-3 top-[-1px] text-[12px] text-blue-700 bg-white px-1 leading-none pointer-events-none sm:hidden">Complemento</label>
                            <div class="w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 md:w-auto md:rounded-none md:ring-0 md:px-0 md:py-0 md:text-inherit md:bg-transparent">
                                ${item.complemento || ' '}
                            </div>
                        </div>
                        <div class="col-span-12 sm:col-span-2 relative py-2">
                            <label class="absolute left-3 top-[-1px] text-[12px] text-blue-700 bg-white px-1 leading-none pointer-events-none sm:hidden">Bairro</label>
                            <div class="w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 md:w-auto md:rounded-none md:ring-0 md:px-0 md:py-0 md:text-inherit md:bg-transparent">
                                ${item.bairro}
                            </div>
                        </div>
                        <div class="col-span-6 sm:col-span-2 relative py-2">
                            <label class="absolute left-3 top-[-1px] text-[12px] text-blue-700 bg-white px-1 leading-none pointer-events-none sm:hidden">Município</label>
                            <div class="w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 md:w-auto md:rounded-none md:ring-0 md:px-0 md:py-0 md:text-inherit md:bg-transparent">
                                ${item.localidade}
                            </div>
                        </div>
                        <div class="col-span-6 sm:col-span-1 relative py-2">
                            <label class="absolute left-3 top-[-1px] text-[12px] text-blue-700 bg-white px-1 leading-none pointer-events-none sm:hidden">UF</label>
                            <div class="w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 md:w-auto md:rounded-none md:ring-0 md:px-0 md:py-0 md:text-inherit md:bg-transparent">
                                ${item.uf}
                            </div>
                        </div>
                        <div class="col-span-6 sm:col-span-1 relative py-2">
                            <label class="absolute left-3 top-[-1px] text-[12px] text-blue-700 bg-white px-1 leading-none pointer-events-none sm:hidden">CEP</label>
                            <div class="w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 md:w-auto md:rounded-none md:ring-0 md:px-0 md:py-0 md:text-inherit md:bg-transparent">
                                ${item.cep}
                            </div>
                        </div>
                        <div class="col-span-6 sm:col-span-1 relative py-2 text-center">
                            <label class="absolute left-3 top-[-1px] text-[12px] text-blue-700 bg-white px-1 leading-none pointer-events-none sm:hidden">Ação</label>
                            <a href="#" class="inline-flex items-center rounded-md px-2.5 py-1.5 text-sm font-medium bg-blue-500 text-white hover:bg-blue-600"
                                 onclick='preencherFormularioRes(${JSON.stringify(item)})'>
                                <i class="bi bi-check2"></i>
                            </a>
                        </div>
                    `;

                    containerResultados.appendChild(div);
                });
            }
        } catch (erro) {
            console.error("Erro ao buscar endereço:", erro);
        }
    }

    // 'input' funciona melhor que 'change' para busca dinâmica
    inputEndereco.addEventListener("input", function () {
        headerResultados.style.display = 'grid'; // Mostra o cabeçalho quando começar a digitar
        // Mostra indicador de carregamento
        containerResultados.innerHTML = `
            <div class="flex items-center gap-2 text-gray-600">
                <svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                </svg>
                <span>Carregando resultados...</span>
            </div>
            `;

        // Debounce simples para não sobrecarregar a API
        clearTimeout(this.delay);
        this.delay = setTimeout(buscarEndereco, 500);
    });

    // Função que insere os valores nos inputs do formulário
    function preencherFormularioRes(item) {
        
        document.getElementById("id_endereco").value = item.logradouro;
        document.getElementById("id_municipio").value = item.localidade;
        document.getElementById("id_uf").value = item.uf;
        document.getElementById("id_cep").value = item.cep;
        document.getElementById("id_bairro").value = item.bairro;

        window.dispatchEvent(new CustomEvent('fechar-modal'));
       
    }