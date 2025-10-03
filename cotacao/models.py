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
    cep = models.CharField(max_length=8)
    telefone = models.CharField(max_length=20)
    dataCadastro = models.DateField(auto_now_add=True)
    dataAtualizacao = models.DateField(auto_now=True)
    email = models.EmailField(unique=True)
    situacao = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.razaoSocial} ({self.cnpj})"
    

class Rota(models.Model):
    idRota = models.AutoField(primary_key=True)
    codRota = models.IntegerField(unique=True)
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    km = models.IntegerField()

    def __str__(self):
        return f"Rota {self.codRota}: {self.origem} → {self.destino}"



class CadVeic(models.Model):
    idVeic = models.AutoField(primary_key=True)
    tpVeiculo = models.CharField(max_length=100)
    tpVeiculoQualp = models.CharField(max_length=100, null=True, blank=True)
    eixos = models.IntegerField()

    def __str__(self):
        return f"{self.tpVeiculo} - {self.eixos} eixos"


class CotacaoBid(models.Model):
    idCotacaoBid = models.AutoField(primary_key=True)
    nCotacaoBid = models.CharField(max_length=50, unique=True, verbose_name="Número da Cotação")
    cliente = models.ForeignKey(CadCliente, on_delete=models.CASCADE)
    dataCriacao = models.DateField(auto_now_add=True)
    rounds = models.IntegerField()

    def __str__(self):
        return f"Cotação {self.nCotacaoBid} - {self.cliente.razaoSocial}"




class DetalheCotacaoBid(models.Model):
    idDetCotBid = models.AutoField(primary_key=True)
    cotacao = models.ForeignKey(CotacaoBid, on_delete=models.CASCADE, related_name="detalhes")
    codRota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    cliente = models.ForeignKey(CadCliente, on_delete=models.CASCADE)
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    tpVeiculoQualp = models.CharField(max_length=100)
    cadVeiculo = models.ForeignKey(CadVeic, on_delete=models.CASCADE)
    eixos = models.IntegerField()
    km = models.IntegerField()
    pedagio = models.DecimalField(max_digits=10, decimal_places=2)
    freteMinimo = models.DecimalField(max_digits=12, decimal_places=2)
    round1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round3 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round4 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    round5 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Detalhe Cotação {self.idDetCotBid} - {self.cliente.razaoSocial}"










