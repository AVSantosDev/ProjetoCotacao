from django.db import models


class CadCliente(models.Model):
    idCliente = models.AutoField(primary_key=True)
    razaoSocial = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    inscEstadual = models.CharField(max_length=20, null=True, blank=True)
    inscMunicipal = models.CharField(max_length=20, null=True, blank=True)
    logradouro = models.CharField(max_length=255)
    numeroLogradouro = models.CharField(max_length=10)  # pode ser "100A"
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    sgEstado = models.CharField(max_length=2)
    pais = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=20)
    dataCadastro = models.DateField(auto_now_add=True)
    dataAtualizacao = models.DateField(auto_now=True)
    email = models.EmailField(unique=True)
    situacao = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.razaoSocial} ({self.cnpj})"
    


class CadVeic(models.Model):
    idVeic = models.AutoField(primary_key=True)
    tpVeiculo = models.CharField(max_length=100)
    tpVeiculoQualp = models.CharField(max_length=100, null=True, blank=True)
    eixos = models.IntegerField()

    def __str__(self):
        return f"{self.tpVeiculo} - {self.eixos} eixos"



class tabelaANTT(models.Model):

    idTabelaANTT = models.AutoField(primary_key=True)
    codTabelaANTT = models.CharField(max_length=8, unique=True, null=True, blank=True)
    Descricao = models.CharField(max_length=255, unique= True, null=True, blank=True)

    def __str__(self):
        return super().__str__()



class CotacaoBid(models.Model):
    idCotacaoBid = models.AutoField(primary_key=True)
    nCotacaoBid = models.CharField(max_length=50, unique=True, verbose_name="Número da Cotação")
    dataCriacao = models.DateField(auto_now_add=True)
    rounds = models.IntegerField(null=True)
    tabelaANTT = models.ForeignKey(tabelaANTT, null=True, blank=True, on_delete=models.CASCADE)
    idCliente = models.ForeignKey(CadCliente, on_delete=models.CASCADE )
    destacado = models.BooleanField(default=False)


    def __str__(self):
        return f"Cotação {self.nCotacaoBid} - {self.cliente.razaoSocial}"




class DetalheCotacaoBid(models.Model):
    idDetCotacao = models.AutoField(primary_key=True)
    codRota = models.CharField(max_length=255)
    cliente = models.ForeignKey(CadCliente, on_delete=models.CASCADE)
    origem = models.CharField(max_length=255, null=True, blank=True)
    destino = models.CharField(max_length=255, null=True, blank=True)
    tpVeiculoQualp = models.CharField(max_length=100)
    cadVeiculo = models.ForeignKey(CadVeic, on_delete=models.CASCADE)
    eixos = models.IntegerField(null=True, blank=True)
    km = models.IntegerField (null=True, blank=True)
    pedagio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    freteMinimo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round3 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round4 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round5 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    ##bid_id = models.ForeignKey()
    cotacao = models.ForeignKey(CotacaoBid, on_delete=models.CASCADE, related_name="detalhes")
    def __str__(self):
        return f"Detalhe Cotação {self.idDetCotBid} - {self.cliente.razaoSocial}"










