document.addEventListener('DOMContentLoaded', function() {
    if (typeof livro !== 'undefined') {
        document.getElementById('titulo').value = livro.titulo || '';
        document.getElementById('autor').value = livro.autor || '';
        document.getElementById('editora').value = livro.editora || '';


        if (livro.capa_url) {
            const capaField = document.getElementById('capa');
            const capaLabel = capaField.nextElementSibling;
            if (capaLabel) {
                capaLabel.insertAdjacentHTML('afterend', `<p>Capa atual: ${livro.capa_url}</p>`);
            }
        }
        if (livro.livro_url) {
            const livroField = document.getElementById('livro');
            const livroLabel = livroField.nextElementSibling;
            if (livroLabel) {
                livroLabel.insertAdjacentHTML('afterend', `<p>Livro atual: ${livro.livro_url}</p>`);
            }
        }
    }
});
