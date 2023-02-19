Select * from PortfolioProject..CovidDeaths
Where continent is not null
order by 3,4

--Select * from PortfolioProject..CovidVaccinations
--order by 3,4

Select location, date, total_cases, new_cases, total_deaths, population from PortfolioProject..CovidDeaths
order by 1,2

--Checking the death percentage

Select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as deathPercentage from PortfolioProject..CovidDeaths
Where location like '%states%'
order by 1,2

--Checking the infected population percentage

Select location, date, population, total_cases, (total_cases/population)*100 as deathPercentage from PortfolioProject..CovidDeaths
Where location like '%states%' and (total_cases/population)*100>10
order by 1,2

--which contry has the highest infection rate compared to population

Select Location, population, Max(total_cases)as hightestInfectionCount, Max((total_cases/population))*100 as PercentPopulationInfected from PortfolioProject..CovidDeaths
Group by location, population
order by PercentPopulationInfected Desc

--which contry has the highest death rate compared to Population cast(total_deaths as int)

Select Location, Max(cast(total_deaths as int))as TotalDeathCount from PortfolioProject..CovidDeaths
Where continent is not null
Group by location
order by TotalDeathCount Desc

-- By Continent

Select Location, Max(cast(total_deaths as int))as TotalDeathCount from PortfolioProject..CovidDeaths
Where continent is null
Group by location
order by TotalDeathCount Desc

-- Total cases by each day

Select date, sum(new_cases) as Total_cases
, sum(cast(new_deaths as int)) as Total_Deaths
, sum(cast(new_deaths as int))/sum(new_cases) as deathpercentage
from PortfolioProject..CovidDeaths
where continent is not null
group by date
order by 1,2


Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations, Sum(
cast(vac.new_vaccinations as bigint))Over (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
order by 2,3


With PopvsVac (location, continent, date, population, new_vaccinations, RollingPeopleVaccinated) 
as
(
Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations, Sum(
cast(vac.new_vaccinations as bigint))
Over (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not Null
--order by 2,3 
)
Select *,(RollingPeopleVaccinated/Population)*100
from PopvsVac

Drop Table if exists #PercentPopulationVaccinated
Create table #PercentPopulationVaccinated
(location nvarchar(255),
Continent nvarchar(255),
Date datetime,
Population Numeric,
new_vaccinations Numeric,
RollingPeopleVaccinated Numeric)

Insert into #PercentPopulationVaccinated
Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations, Sum(
cast(vac.new_vaccinations as bigint))
Over (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not Null
--order by 2,3 
Select *,(RollingPeopleVaccinated/Population)*100
from #PercentPopulationVaccinated


Create view PercentPopulationVaccinated
as
Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations, Sum(
cast(vac.new_vaccinations as bigint))
Over (Partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not Null