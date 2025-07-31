import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Download, Star, TrendingUp, Users, Calendar, ShoppingCart, RotateCcw, Headphones, HelpCircle } from 'lucide-react'

function AdminDashboard() {
  const [responses, setResponses] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      
      // Buscar todas as respostas
      const responsesRes = await fetch('/api/csat')
      if (!responsesRes.ok) throw new Error('Erro ao buscar respostas')
      const responsesData = await responsesRes.json()
      
      // Buscar estatísticas
      const statsRes = await fetch('/api/csat/stats')
      if (!statsRes.ok) throw new Error('Erro ao buscar estatísticas')
      const statsData = await statsRes.json()
      
      setResponses(responsesData)
      setStats(statsData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const exportToCSV = async () => {
    try {
      const response = await fetch('/api/csat/export')
      if (!response.ok) throw new Error('Erro ao exportar dados')
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = `csat_dados_${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      alert('Erro ao exportar dados: ' + err.message)
    }
  }

  const getRatingBadge = (rating) => {
    const colors = {
      1: 'bg-red-500',
      2: 'bg-orange-500', 
      3: 'bg-yellow-500',
      4: 'bg-blue-500',
      5: 'bg-green-500'
    }
    
    const labels = {
      1: 'Muito Insatisfeito',
      2: 'Insatisfeito',
      3: 'Neutro',
      4: 'Satisfeito',
      5: 'Muito Satisfeito'
    }

    return (
      <Badge className={`${colors[rating]} text-white`}>
        {rating} ⭐ - {labels[rating]}
      </Badge>
    )
  }

  const getContextIcon = (context) => {
    if (!context) return <HelpCircle className="w-4 h-4" />
    
    const contextLower = context.toLowerCase()
    if (contextLower.includes('compra')) return <ShoppingCart className="w-4 h-4" />
    if (contextLower.includes('devolução')) return <RotateCcw className="w-4 h-4" />
    if (contextLower.includes('suporte') || contextLower.includes('assistência')) return <Headphones className="w-4 h-4" />
    return <HelpCircle className="w-4 h-4" />
  }

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('pt-BR')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando dados...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center text-red-600">
              <p className="font-semibold">Erro ao carregar dados</p>
              <p className="text-sm mt-2">{error}</p>
              <Button onClick={fetchData} className="mt-4">
                Tentar Novamente
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard CSAT</h1>
            <p className="text-gray-600">Painel administrativo de avaliações de atendimento</p>
          </div>
          <Button onClick={exportToCSV} className="bg-green-600 hover:bg-green-700">
            <Download className="w-4 h-4 mr-2" />
            Exportar CSV
          </Button>
        </div>

        {/* Estatísticas */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total de Avaliações</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_responses}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Média Geral</CardTitle>
                <Star className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.average_rating}</div>
                <p className="text-xs text-muted-foreground">de 5.0 estrelas</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Satisfação Alta</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.rating_distribution[4] + stats.rating_distribution[5]}
                </div>
                <p className="text-xs text-muted-foreground">avaliações 4-5 estrelas</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Última Atualização</CardTitle>
                <Calendar className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-sm font-bold">{new Date().toLocaleString('pt-BR')}</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Distribuição por Rating */}
        {stats && (
          <Card>
            <CardHeader>
              <CardTitle>Distribuição por Avaliação</CardTitle>
              <CardDescription>Quantidade de avaliações por número de estrelas</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[5, 4, 3, 2, 1].map(rating => (
                  <div key={rating} className="flex items-center space-x-3">
                    <div className="w-20 text-sm font-medium">
                      {rating} ⭐
                    </div>
                    <div className="flex-1 bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                        style={{ 
                          width: stats.total_responses > 0 
                            ? `${(stats.rating_distribution[rating] / stats.total_responses) * 100}%` 
                            : '0%' 
                        }}
                      ></div>
                    </div>
                    <div className="w-12 text-sm text-gray-600">
                      {stats.rating_distribution[rating]}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Tabela de Respostas */}
        <Card>
          <CardHeader>
            <CardTitle>Todas as Avaliações</CardTitle>
            <CardDescription>Lista completa das avaliações recebidas</CardDescription>
          </CardHeader>
          <CardContent>
            {responses.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p>Nenhuma avaliação encontrada</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Contexto</TableHead>
                      <TableHead>Avaliação</TableHead>
                      <TableHead>Comentário</TableHead>
                      <TableHead>Data/Hora</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {responses.map((response) => (
                      <TableRow key={response.id}>
                        <TableCell className="font-medium">#{response.id}</TableCell>
                        <TableCell>
                          <div className="flex items-center space-x-2">
                            {getContextIcon(response.context)}
                            <span className="text-sm">
                              {response.context || 'Não especificado'}
                            </span>
                          </div>
                        </TableCell>
                        <TableCell>{getRatingBadge(response.rating)}</TableCell>
                        <TableCell className="max-w-xs">
                          {response.comment ? (
                            <div className="truncate" title={response.comment}>
                              {response.comment}
                            </div>
                          ) : (
                            <span className="text-gray-400 italic">Sem comentário</span>
                          )}
                        </TableCell>
                        <TableCell>{formatDate(response.timestamp)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default AdminDashboard

